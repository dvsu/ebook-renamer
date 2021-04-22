# Ebook Renamer

### **Introduction**
<br>

Who doesn't like cheap ebooks on Humble Bundle? I know it is too good to miss, so do you :) <br>
Your ebook collection is slowly growing and starts filling up your storage. Let say you quickly scan through a collection of 30 ebooks for an ebook you are interested in.
Perhaps it is not a problem at all. What about 100? 1000? or 10000?<br>

Personally, I think the default ebook title is not really readable because it lacks proper punctuations as shown on your Humble Bundle purchase page.
If you compare the title on the left column of table below and the corrected title on the right, you may agree with me that the one on the right is much more readable.<br> 

|Default Ebook Title<br>(after download) | Corrected Ebook Title<br>(as on website) |
|:--------------------------------------:|:-------------------:|
|`thisisanebook` |`This is an eBook`|

So, what are you going to do to reorganize your collection? *Rename! (yes, I hear you)*<br> 
Imagine renaming the ebooks one by one and feel frustrated after several iterations. Then you are not alone. I used to do it until I reached a point that I had had enough and really needed an automation. 
Hence, this simple script is created.
<br>
<br>


### **Guides**
<br>

1. Go to your Humble Bundle purchases and select one of your ebook bundles on purchased product list.
2. Copy the titles that we wish to apply on downloaded ebooks.

<p align="center">
  <img width="30%" height="30%" src="/images/resource.PNG">
</p>

3. List the ebook titles in a file and save it as reference file.

<p align="center">
  <img width="50%" height="50%" src="/images/reference.PNG">
</p>

4. Open `main.py` and type the location of both reference file and folder where ebooks are located. 
    ```python
    from file_renamer import FileRenamer


    # path of file that contains list of corrected ebook titles
    REFERENCE_PATH = '/path/to/reference/file'

    # path of directory that contains list of ebooks that have not been renamed
    FILE_PATH = '/path/to/ebook/folder'


    fr = FileRenamer(reference_path=REFERENCE_PATH, file_path=FILE_PATH)

    ```

5. Execute the `main.py` script on terminal. Remember that the `main.py` requires `file_renamer.py` to work properly.

5. Witness the magic how the script renames the ebooks instantly
<br>
<br>

#### **Before**
<br>

<p align="center">
  <img width="50%" height="50%" src="/images/before.PNG">
</p>
<br>

#### **After**
<p align="center">
  <img width="50%" height="50%" src="/images/after.PNG">
</p>
<br>
<br>

### **TODO**
<br>

1. Create CLI command to simplify the task without messing around with the content of script
2. Design and integrate with GUI to simplify the renaming task by selecting directory and file paths instead of typing manually
3. Create executable file derived from the script to make it portable and user-friendly
