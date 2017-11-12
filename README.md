# version_parser
This program will return the url of the newest version of software available from a url.
The program will work by default against software that follows the pattern from the 
Semantic Version 2.0.0 specification (http://semver.org).

Directory browsing must be enabled on the remote software repository
as the contents of the HTML from the url are parsed.
( Most repositories should have this enabled )

Ex.
If you are downloading software from the url https://mysoftware.com/stable
and the downloadable files have the consistent naming scheme of mysoftware-x.x.x.tar.gz
then you will provide the following arguments to the script:
url = 'https://mysoftware.com/stable'
prefix = 'mysoftware-'
suffix = '.tar.gz'

If there were only three versions available (1.0.0, 1.0.1, 1.1.0)
Then the program would return the following url:
'https://mysoftware.com/stable/mysoftware-1.1.0.tar.gz'

The program is designed to provide a dynamic download for tools like curl, or Ansible.
Note that the output will likely need to be trimmed of newlines 
by the program that uses these results
