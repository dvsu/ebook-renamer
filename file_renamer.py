import os
import platform


class FileCheck:

    def __init__(self, reference_path:str, file_path:str):
        self.delim_char = '/' if platform.system() == 'Linux' else '\\'
        self.check_path([reference_path, file_path])


    # Check the existence of path/ directory. If any of them does not exist, exit the program
    def check_path(self, path_list:str) -> None:
        
        for path in path_list:
            if not os.path.exists(path):
                raise FileNotFoundError(f"'{path}' does not exist")


class FileNames:

    def __init__(self, reference_path:str, file_path:str):
        self.ref_path = reference_path
        self.ref_dir = self.get_reference_directory(reference_path)
        self.ref_name = self.get_reference_name(reference_path)
        self.file_path = file_path
        self.recognized_formats = ['epub', 'pdf', 'mobi', 'prc', 'docx']
        self.raw_file_list = os.listdir(file_path)
        self.document_names = self.get_document_names()
        self.raw_file_name_mapping = self.get_raw_file_name_mapping()
        self.renamed_raw_file_check_flag = self.get_raw_file_check_flag()
        self.document_keywords = self.get_document_keywords()


    # This method will convert a string to lowercase and remove any special characters listed below
    def rename_to_plain_lowercase(self, text:str) -> str:
        replaced_chars = "\\`*_{}[]()>#+-.,!$"

        for c in replaced_chars:
            if c in text:
                text = text.replace(c, '')
        
        # If "&" character exists, replace it with "and" to assist in keyword matching
        text = text.replace("&", "and") if "&" in text else text

        return text.lower()


    def get_reference_directory(self, reference_path:str) -> str:

        # If directory separator, e.g. / or \ exists in reference path, the directory name will be splitted into multiple strings.
        # Otherwise, the output will be a string list with a single element
        # path will be the full directory name on top of reference file. Otherwise, it return an empty string
        return self.delim_char.join(reference_path.split(self.delim_char)[:-1])


    def get_reference_name(self, reference_path:str) -> str:

        # If directory separator, e.g. / or \ exists in reference path, the directory name will be splitted into multiple strings.
        # Otherwise, the output will be a string list with a single element. Thus, filename should exist regardless the directory path.
        return reference_path.split(self.delim_char)[-1]


    def get_document_names(self) -> list:

        data = []

        # The printed directory name is 'current directory' if the reference path is an empty string, i.e. current directory.
        # Otherwise print the whole path
        directory = "current directory" if self.ref_dir else f"directory '{self.ref_dir}'"
        print(f"Listing book titles from reference file '{self.ref_name}' at {directory}")

        with open(self.ref_path, 'r') as file:
            
            title_count = 0

            for count, title in enumerate(file, 1):

                # Some ebook titles may contain colon ':', which is an invalid character in Windows file system.
                # To prevent this from occuring, the colon is replaced with a white space and a hyphen ' -'
                # to create separation between the main title and subtitle.
                formatted_title = title.replace(':', ' -').strip()
                print(f"{count}. {formatted_title}")
                data.append((len(formatted_title), formatted_title))
                title_count = count

            print(f"Found {title_count} title(s)")
            
        # Sort by length in descending order, to prioritize files with longer keywords.
        # As there is a possibility of shorter file name exists in longer file name, e.g. "A Complete Guide" and "A Complete Guide to Everything"
        # file with longer name will be renamed first to prevent possible duplication
        data = sorted(data, reverse=True)
        _, document_names = zip(*data)

        return document_names


    def get_raw_file_name_mapping(self) -> dict:
        # create a mapping of original raw name and renamed raw name
        # original raw name is used for file lookup in directory for renaming task
        # renamed raw name is used for keyword search

        renamed_raw_files = {}

        for raw_file in self.raw_file_list:

            # split the filename into two and store them in 2 variables, 
            #  "name" which stores the unmodified filename and 
            #  "file_format" which stores the file format of that particular file
            name, file_format= raw_file.split('.')

            renamed = self.rename_to_plain_lowercase(name).replace(' ', '')
            
            if file_format in self.recognized_formats:
                renamed_raw_files[raw_file] = f"{renamed}.{file_format}"

        return renamed_raw_files


    def get_raw_file_check_flag(self) -> dict:

        file_check_flag = {}

        # the keys contain the original raw name and values contains the renamed raw name
        for original_raw_file, renamed_raw_file in self.raw_file_name_mapping.items():
            renamed, file_format = renamed_raw_file.split('.')

            file_check_flag[f"{renamed}.{file_format}"] = True if original_raw_file in self.document_names else False

        return file_check_flag


    def get_document_keywords(self) -> dict:

        return {document: self.rename_to_plain_lowercase(document).split(' ') for document in self.document_names}
        


class FileRenamer(FileCheck, FileNames):

    def __init__(self, reference_path:str, file_path:str=''):
        FileCheck.__init__(self, reference_path, file_path)
        FileNames.__init__(self, reference_path, file_path)
        self.omitted_words = ["the"]
        self.run()


    def keyword_check(self, keywords:list, renamed_raw_name:str) -> bool:

        print(f"Checking keywords '{keywords}' in {renamed_raw_name}")

        matched_words = 0

        index = 0
        for keyword in keywords:
            nchar = len(keyword)
            
            # If keyword matches, find the next keyword. Otherwise, it is mismatched and return False
            if (keyword == renamed_raw_name[index:index+nchar]):
                index += nchar
                matched_words += 1
            
            # There is also a case when the expected name may contain one of the omitted words, e.g. "the"
            # when the raw name may not. In this case, it is assumed the word is not an important keyword,
            # and continue to check the next keywords.
            elif keyword in self.omitted_words:
                continue

            else:
                # renamed_raw_name may be shortened from its full title. In this case, this if-else statement could mistakenly flag it
                # as "mismatched keyword", in fact, there is no more word to check at the end of renamed_raw_name, i.e. indicating
                # that the renamed_raw_name is shortened. In this case, as long as the length of renamed_raw_name = index
                # i.e. has been fully checked and matched until the end, it is considered a "match"
                if len(renamed_raw_name) == index: 
                    return True
                else: 
                    return False

        # if keyword check has been completed and able to exit the loop successfully
        # it indicates the keywords are 100% match. Thus, return True
        return True

    def rename_file(self, check_name:str, old_name:str, new_name:str, file_format:str) -> None:
        
        try:
            base_path = f"{self.file_path}{self.delim_char}"
            os.rename(f"{base_path}{old_name}.{file_format}", f"{base_path}{new_name}.{file_format}")
            self.renamed_raw_file_check_flag[f"{check_name}.{file_format}"] = True
            print(f"Renamed file from '{old_name}.{file_format}' to '{new_name}.{file_format}'")

        except FileExistsError:
            print(f"Duplicated name found. '{new_name}.{file_format}' exists. Target file for renaming is '{old_name}.{file_format}'")


    def run(self):
        
        for document, keywords in self.document_keywords.items():

            for original_raw_file, renamed_raw_file in self.raw_file_name_mapping.items():
                # Skip checking if the check_flag is True, i.e. document has been properly renamed
                if self.renamed_raw_file_check_flag[renamed_raw_file]: continue
                
                # renamed_raw_name is used for keyword check
                # original_raw_name is used for file name lookup for renaming task
                renamed_raw_name, file_format = renamed_raw_file.split('.')
                original_raw_name, _ = original_raw_file.split('.')
                if self.keyword_check(keywords=keywords, renamed_raw_name=renamed_raw_name):
                    self.rename_file(check_name=renamed_raw_name, old_name=original_raw_name, new_name=document, file_format=file_format)
                
                else:
                    print(f"{'-'*3} Skipped. Renamed check flag:{self.renamed_raw_file_check_flag[renamed_raw_file]}")
