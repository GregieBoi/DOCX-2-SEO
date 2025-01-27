# DOCX-2-SEO

## What is this?
DOCX-2-SEO is a desktop application built using Python and PyQT6 utilizing the BeautifulSoup4 and Mammoth Python libraries to convert formatted Microsoft Word documents (.docx) into properly styled HTML documents (.html) with added buttons and images to be published as blogs on client websites.

## Creating a Client
Clients hold styling, formatting, and other information to be used for generating the HTML document. You can create a client in the client tab by following these steps:

1. Select "New Client" from the dropdown menu.

2. Enter the name of the client into the "Name" field.

3. Enter the html code for the button you would like to appear in the document. The button code can be of any format so long it contains an <a> tag.

4. Enter any styling information on a per tag basis using the JSON format. For example, if you only wanted to style all <p> tags such that they were 14px in size, bold, and red, you would enter the following code:
```
{
    "p": {
        "font-size": "14px",
        "font-weight": "bold",
        "color": "red"
    }
}
```
5. Enter the content section wrapper html code for the document. By default, this is set to <div><div></div></div>. If further styling is needed, you can edit the properties of each div tag as you see fit. The wrapper code must contain two div tags with one nested inside the other.

6. Click "Save" to save the client.

## Creating a Topic
Topics hold image src links, alt text, and redirect links to allow for automatic generation of the HTML document. You can create a topic in the topics tab by following these steps:

1. Select "New Topic" from the dropdown menu.

2. Enter the name of the topic into the "Name" field.

3. Enter the redirect link for the topic in the "Link" field.

4. Images are seperated into 4 different categories to help decide where to best place it based on the blog content: Hero, Tech, Interior, and Misc. Add a src link for a category by clicking the + button and entering the src link into the respective field.

5. After adding all img src links for the topic, click "Save"

## Generating a HTML Document
Generating a HTML document is the process of converting the DOCX file into a properly styled HTML document with added buttons and images. You can generate a document in the generate tab by following these steps:

1. After launching the application, upload the DOCX file you want to convert in the generate tab.

2. Once the file is uploaded, select the client that you want to style the final HTML document for. 

3. Select the generation type you want to use: Manual or Automatic. 

3.1 Manual: Enter the text you would like to appear in any buttons (Defaults to "View Inventory") and the link you would like the buttons to lead to, click the "Generate" button, input the alt text and src links for any images you would like to have in the document, click submit, then save the file.

3.2 Automatic: Select the blog topic you would like to use for the document from the dropdown menu, if you would like to change the button text and link enter desired text and link into the respective fields, click "Generate" and then save the file. 

## Editing a Client
Editing a client is the same as creating a client, except you can edit the existing client by selecting it from the dropdown menu and clicking "Save" after making changes.

## Editing a Topic
Editing a topic is the same as creating a topic, except you can edit the existing topic by selecting it from the dropdown menu and clicking "Save" after making changes. 

## Deleting a Client
Deleting a client is simple and straightforward. Select the client you would like to delete from the dropdown menu and click "Delete" to remove it from the list.

## Deleting a Topic
Deleting a topic is simple and straightforward. Select the topic you would like to delete from the dropdown menu and click "Delete" to remove it from the list.