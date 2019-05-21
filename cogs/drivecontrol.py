from __future__ import print_function
import discord
from discord.ext import commands
import misc
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER = 'application/vnd.google-apps.folder'

def plexembed(title, description, color = discord.Color.gold()):
    return discord.Embed(color = color, title= title, description=description)

def search(service, string):

    items = []
    nextPage = True
    nextPageToken = ''

    while nextPage == True:
                                      

        folderList = service.files().list(pageToken=nextPageToken, pageSize=1000, fields="nextPageToken, files(id, name, ownedByMe)", 
            q="mimeType = 'application/vnd.google-apps.folder' and name contains '{}'".format(string)).execute()

        if 'nextPageToken' in folderList:
            nextPageToken = folderList['nextPageToken']
        else:
            nextPage = False

        items = items + folderList['files']

    return items


def iterfiles(service, name=None, is_folder=None, parent=None, order_by='folder,name,createdTime'):
    q = []
    if name is not None:
        q.append("name = '%s'" % name.replace("'", "\\'"))
    if is_folder is not None:
        q.append("mimeType %s '%s'" % ('=' if is_folder else '!=', FOLDER))
    if parent is not None:
        q.append("'%s' in parents" % parent.replace("'", "\\'"))
    params = {'pageToken': None, 'orderBy': order_by}
    if q:
        params['q'] = ' and '.join(q)
    while True:
        response = service.files().list(**params).execute()
        for f in response['files']:
            yield f
        try:
            params['pageToken'] = response['nextPageToken']
        except KeyError:
            return

def walk(top, service):
    top, = iterfiles(service, name=top, is_folder=True)
    stack = [((top['name'],), top)]
    while stack:
        path, top = stack.pop()
        dirs, files = is_file = [], []
        for f in iterfiles(service, parent=top['id']):
            is_file[f['mimeType'] != FOLDER].append(f)
        yield path, top, dirs, files
        if dirs:
            stack.extend((path + (d['name'],), d) for d in dirs)
            
def main(searchterm):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    
    result = search(service, searchterm)
    ownedresults = []
    unownedresults = []
    for i in result:
        if i['ownedByMe'] == True:
            ownedresults.append(i)
        else:
            unownedresults.append(i)

    returntext = ''

    
    permission = {"role": "reader", "type": "anyone"}
    for item in ownedresults:
        try:
            service.permissions().create(fileId=item['id'], body=permission).execute()
            link = service.files().get(fileId=item['id'], fields='webViewLink').execute()['webViewLink']
            returntext += '{} : {}\n'.format(item['name'], link)
        except:
            returntext += "Cannot share this file: {}".format(item['name'])

    returntext += "Found {} matches in your google drive which you do not own.".format(len(unownedresults))
                  
    return returntext

class DriveControl:
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='drive')
    async def drivelookup(self, ctx, *, search):
        """Get Drive Link if applicable"""
        await ctx.send(embed=plexembed("Google Drive Results:", main(search)))


def setup(bot):
    bot.add_cog(DriveControl(bot))
