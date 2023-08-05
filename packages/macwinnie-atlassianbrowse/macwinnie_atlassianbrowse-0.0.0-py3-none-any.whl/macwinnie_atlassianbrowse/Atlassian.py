#!/usr/bin/env python3

import requests, os, json, time, re, gc, getpass
import urllib.parse
import pyotp

from datetime     import datetime

from bs4          import BeautifulSoup
from urllib       import parse
from urllib.parse import parse_qs
from urllib.parse import urlparse

from macwinnie_pyhelpers.Browser import Browser

from selenium                                       import webdriver
from selenium.common.exceptions                     import NoSuchElementException
from selenium.webdriver.common.keys                 import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by                   import By
from selenium.webdriver.support.wait                import WebDriverWait
from selenium.webdriver.support                     import expected_conditions as EC
from selenium.webdriver.common.action_chains        import ActionChains

class Atlassian ( Browser ):
    """Special functions for Atlassian systems – they need to have `nosso` active at least ..."""

    def webSudo( self, authUrl, sysInfoUrl, adjustCookies = True ):
        """run the application webSudo"""
        if not self.checkLogin():
            self.login()
        self.browser.get( sysInfoUrl )
        pwFieldXPath = '//input[@type="password"]'
        doWebSudo = (
                        self.browser.current_url != sysInfoUrl
                    ) or (
                        self.checkElementByXpath( pwFieldXPath )
                    )
        if doWebSudo:
            self.browser.get( authUrl )
            pwfield = WebDriverWait( self.browser, 10 ).until( EC.presence_of_element_located( ( By.XPATH, pwFieldXPath ) ) )
            pwfield.send_keys( Keys.CONTROL, "a" )
            pwfield.send_keys( self.app[ 'passwd' ] )
            pwfield.send_keys( Keys.ENTER )
            time.sleep( 5 )
            if adjustCookies:
                self.refresh()

    def getToken( self ):
        """get CSRF token of Atlassian App"""
        self.get( self.app['url'] )
        return self.browser.find_element( By.ID, 'atlassian-token' ).get_attribute( 'content' )


class Jira ( Atlassian ):
    """Jira Browser – recommended to use administrative user; otherwise most functions won't work properly"""

    appInfo = {
        "url":    {
            "env":         "JIRA_URL",
            "url":         True,
            "description": "Enter Jira URL",
        },
        "user":   {
            "env":         "JIRA_USER",
            "description": "Enter Jira username",
        },
        "passwd": {
            "password":    True,
            "env":         "JIRA_PASS",
            "description": "Enter Jira password",
        },
    }

    projectKeys  = []
    permissions  = {}
    projectLeads = {}

    def __init__( self ):
        super( Jira, self ).__init__()

    def setSessionBaseHeaders( self, api=False ):
        """Api requests need special headers in Jira ... sometimes ..."""
        if not api:
            self.sessionBaseHeaders = None
        else:
            self.sessionBaseHeaders = {
                "Content-Type":      "application/json",
                "X-Atlassian-Token": "no-check"
            }

    def login( self, skipSSO=True ):
        """Run Jira login"""
        loginUrl = self.app[ 'url' ] + "login.jsp"
        if skipSSO:
            loginUrl += '?nosso'
        self.loadCookies( url=loginUrl )
        self.setSessionBaseHeaders()
        userObject = { "os_username": self.app[ 'user' ], "os_password": self.app[ 'passwd' ], }
        if os.getenv( "PRINT_DEBUG_INFO", "False" ).lower() in [ "1", "true", "t", "y", "yes" ]:
            print( 'User is being logged in with those credentials:' )
            print( userObject )
            print()
        self.sessionPostRequest( loginUrl, userObject, True, urlOverride=True )
        self.get( self.app[ 'url' ] , False )

    def checkLogin( self ):
        """Check if login is needed"""
        currentUrl = self.browser.current_url
        urlLen     = len( self.app[ 'url' ] )
        if currentUrl[ 0:urlLen ] != self.app[ 'url' ]:
            self.get( self.app[ 'url' ], False )
        try:
            self.browser.find_element( By.ID, 'login' )
            return False
        except:
            return True

    def webSudo( self, adjustCookies = True ):
        """Run the Jira WebSudo"""
        authUrl    = '{url}secure/admin/WebSudoAuthenticate!default.jspa'.format( url=self.app[ 'url' ] )
        sysInfoUrl = '{url}secure/admin/ViewApplicationProperties.jspa'.format( url=self.app[ 'url' ] )
        super( Jira, self ).webSudo( authUrl, sysInfoUrl, adjustCookies )

    def getProjectKeys( self ):
        """Get a list of Project Keys of those Jira projects visible to logged in user"""
        self.webSudo()
        self.get( self.app[ 'url' ] + 'secure/project/BrowseProjects.jspa' )
        while True:
            soup = self.toSoup()
            self.projectKeys += [ item.text for item in soup.select( 'tbody tr .cell-type-key' ) ]
            try:
                nextBtn = soup.select( '.aui-nav-next a' )[0]
                check   = nextBtn[ 'data-page' ]
                self.browser.find_element( By.XPATH, '//*[contains(concat(" ", normalize-space(@class), " "), " aui-nav-next ")]//a' ).click()
                time.sleep(5)
            except:
                break
        return self.projectKeys

    def getUserGroups( self, username, session=None ):
        """Function to gather groups of user"""
        apiUrl = '{url}rest/api/2/user?username={user}&expand=groups'.format( url=self.app['url'], user=urllib.parse.quote( username ) )
        groups = self.apiGetInfo( apiUrl, session=session )
        return [ g['name'] for g in groups['groups']['items'] ]

    def getUserApiInfo( self, username, returnResponse=False, session=None ):
        """Function to gather information about a user from API – if `returnResponse` is True, the whole request response is returned, otherwise only the decoded answer object"""
        apiUrl = '{url}rest/api/2/user?username={user}'.format( url=self.app['url'], user=urllib.parse.quote( username ) )
        return self.apiGetInfo( apiUrl, returnResponse, session )

    def getGroupApiInfo( self, groupname, returnResponse=False, session=None ):
        """Function to gather information about a group from API – if `returnResponse` is True, the whole request response is returned, otherwise only the decoded answer object"""
        apiUrl = '{url}rest/api/2/group?groupname={group}'.format( url=self.app['url'], group=urllib.parse.quote( groupname ) )
        return self.apiGetInfo( apiUrl, returnResponse, session )

    def gatherProjectPermissions( self, projectKey, session=None ):
        """Function to gather permissions for a specific Jira project"""
        rolesDropdownXpath = '//*[contains(concat(" ", @class, " "), " iLKsB ")]'
        projectPermissions = None
        self.get( '{url}plugins/servlet/project-config/{pjkey}/roles'.format( url=self.app['url'], pjkey=projectKey ) )
        skip = True
        try:
            WebDriverWait( self.browser, 10 ).until( EC.presence_of_element_located( ( By.XPATH, '//*[contains(concat(" ", @class, " "), " EKGYc ")]' ) ) )
            skip = False
        except:
            print( '{p} skipped'.format( p = projectKey ) )
        if not skip:
            projectPermissions = {}
            continueLookup = True
            # retrieve possible roles
            roleBtn = WebDriverWait( self.browser, 10 ).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat(" ", @class, " "), " css-18u3ks8 ")]')))
            roleBtn.click()
            # wait until dropdown is visible
            WebDriverWait( self.browser, 10 ).until(EC.presence_of_element_located((By.XPATH, rolesDropdownXpath)))
            # kteeYD (selected, single one), goEvqh (selected, multiple ones), eJTYOK (not selected)
            roleElements = self.browser.find_elements( By.XPATH, '//*[contains(concat(" ", @class, " "), " eJTYOk ") or contains(concat(" ", @class, " "), " goEvqh ") or contains(concat(" ", @class, " "), " kteeYD ")]' )
            for rl in roleElements:
                role = re.match( r'^(.+?)(\s\([0-9]+\))?$' ,rl.text ).group( 1 )
                projectPermissions[ role ] = {'USERS':[], 'GROUPS':[]}
            try:
                roleBtn.click()
                WebDriverWait( self.browser, 10 ).until_not(EC.presence_of_element_located((By.XPATH, rolesDropdownXpath)))
            except:
                actions = ActionChains( self.browser )
                actions.send_keys( Keys.ESCAPE )
                actions.perform()
                WebDriverWait( self.browser, 10 ).until_not(EC.presence_of_element_located((By.XPATH, rolesDropdownXpath)))
            while continueLookup:
                # find all username and groupname fields on page
                nameFields = self.browser.find_elements( By.XPATH, '//*[contains(concat(" ", @class, " "), " EKGYc ")]' )
                # fetch users for roles
                for x in nameFields:
                    n = x.text
                    trigger = x.find_element( By.XPATH, './parent::*/parent::*/parent::*/parent::*//*[contains(concat(" ", @class, " "), " css-8xpfx5 ")]' )
                    resp = self.getUserApiInfo( n, True, session )
                    index = None
                    if ( resp.status_code == 200 ):
                        index = 'USERS'
                    else:
                        resp = self.getGroupApiInfo( n, True, session )
                        if ( resp.status_code == 200 ):
                            index = 'GROUPS'
                    if index != None:
                        try:
                            trigger.click()
                            WebDriverWait( self.browser, 10 ).until(EC.presence_of_element_located((By.XPATH, rolesDropdownXpath)))
                            clicked = True
                        except:
                            actions = ActionChains( self.browser )
                            actions.send_keys( Keys.ESCAPE )
                            actions.perform()
                            try:
                                WebDriverWait( self.browser, 10 ).until(EC.presence_of_element_located((By.XPATH, rolesDropdownXpath)))
                            except Exception as e:
                                self.browser.get_screenshot_as_file('./data/debug/error_{index}_open_{date}.png'.format( date = datetime.now().strftime("%Y%m%d_%H%M%S"), index=index ))
                                raise e
                        roleElements = self.browser.find_elements( By.XPATH, '//*[contains(concat(" ", @class, " "), " kteeYD ") or contains(concat(" ", @class, " "), " goEvqh ")]' )
                        for rl in roleElements:
                            projectPermissions[ rl.text ][ index ].append( n )
                        try:
                            trigger.click()
                            WebDriverWait( self.browser, 10 ).until_not(EC.presence_of_element_located((By.XPATH, rolesDropdownXpath)))
                            clicked = True
                        except:
                            actions = ActionChains( self.browser )
                            actions.send_keys( Keys.ESCAPE )
                            actions.perform()
                            try:
                                WebDriverWait( self.browser, 10 ).until_not(EC.presence_of_element_located((By.XPATH, rolesDropdownXpath)))
                            except Exception as e:
                                self.browser.get_screenshot_as_file('./data/debug/error_{index}_close_{date}.png'.format( date = datetime.now().strftime("%Y%m%d_%H%M%S"), index=index ))
                                raise e
                try:
                    self.browser.find_element( By.XPATH, '//*[@aria-label="Next" and not(@disabled)]' ).click()
                except:
                    continueLookup = False
        return projectPermissions

    def getGroups( self ):
        """get list of groupnames existing in Jira"""
        session = self.toSession()
        rspJ = session.get( '{url}rest/api/2/groups/picker?maxResults={limit}'.format( url=self.app[ 'url' ], limit=5000 ) )
        jgroups = []
        if rspJ.status_code == 200:
            rsp = json.loads( rspJ.text )
            for g in rsp['groups']:
                jgroups.append( g[ 'name' ] )
        return jgroups

    def removeUserFromGroup( self, group, user, session=None ):
        """Remove user from group"""
        if session == None:
            session = self.toSession( curl = True )
        requestData = {
            'groupname': group,
            'username':  user
        }
        rsp = session.delete( '{url}rest/api/2/group/user?{params}'.format( url=self.app[ 'url' ], params=urllib.parse.urlencode( requestData ) ) )
        return rsp

    def addUserToGroup( self, group, user, session=None ):
        """Add user to group"""
        if session == None:
            session = self.toSession( curl = True )
        rsp = session.post( '{url}rest/api/2/group/user?groupname={group}'.format(url=self.app['url'], group=group), data = json.dumps({'name':user}), headers={'content-type':'application/json'} )
        return rsp

    def getGroupMembers( self, group, activeFilter='true' ):
        """get group members from GUI"""
        self.webSudo()
        self.setSessionBaseHeaders()
        self.sessionPostRequest( '{url}secure/admin/user/UserBrowser.jspa'.format( url=self.app['url'] ), { 'userSearchFilter': '', 'group': group, 'applicationFilter': '', 'activeFilter': activeFilter, 'max': 1000000 } , True )
        should = WebDriverWait( self.browser, 10 ).until( EC.presence_of_element_located( ( By.XPATH, '//*[contains(concat(" ", @class, " "), " results-count ")]//*[contains(concat(" ", @class, " "), " results-count-total ")]' ) ) ).text
        gms    = self.browser.find_elements( By.XPATH, '//*[@data-cell-type="username"]/ancestor::tr[position() = 1]' )
        if len(gms) != int(should):
            raise Exception('Count-Missmatch with group members of "{g}": {f} found, but {s} should have!'.format(g=group, f=len(gms), s=should))
        users = []
        for i in gms:
            users.append( i.get_attribute( "data-user" ) )
        return users

    def getGroupMembersAPI( self, group ):
        """get group members from API – sometimes a little bit buggy ..."""
        sessionJ = self.toSession()
        stop = False
        i = 0
        users = []
        while True:
            limit = 50
            parameters = {
                'groupname': group,
                'startAt': ( i * limit ),
                'maxResults': limit,
                'includeInactiveUsers': 'false',
            }
            memberUrl = '{url}rest/api/2/group/member?{params}'.format( url=self.app[ 'url' ], params=urllib.parse.urlencode( parameters ) )
            rspJ = sessionJ.get( memberUrl )

            if rspJ.status_code == 200:
                rsp = json.loads( rspJ.text )
                if rsp[ 'isLast' ] == True:
                    stop = True
                for u in rsp['values']:
                    users.append( u[ 'name' ] )
            else:
                print('rc: ' + str(rspJ.status_code))
                print(parameters)
                stop = True

            if stop or len( rsp['values'] ) == 0:
                len( rsp['values'] )
                break
            else:
                i += 1
        return users

    def getActiveProjectLead( self, projectKey, session=None ):
        """Function to retrieve project lead of Jira project, if the user is still active"""
        if session == None:
            session = self.toSession()
        self.browser.get( '{url}plugins/servlet/project-config/{pjkey}/roles'.format( url=self.app['url'], pjkey=projectKey ) )
        plo = WebDriverWait( self.browser, 10 ).until( EC.presence_of_element_located( ( By.XPATH, '//*[contains(concat(" ", @class, " "), " jKQrhX ")]//a' ) ) )
        parsedProfile = urlparse( plo.get_attribute('href') )
        ploUser = parse_qs(parsedProfile.query)['name'][0]
        resp = session.get( '{url}rest/api/2/user?username={user}'.format( url=self.app['url'], user=urllib.parse.quote( ploUser ) ) )
        try:
            userJson = json.loads( resp.text )
            active = userJson['active']
        except:
            active = False
        if ( resp.status_code == 200 and active):
            return ploUser
        else:
            return None

    def getProjectLeads( self ):
        """Function to retrieve active project leads for all Jira projects"""
        if len( self.projectKeys ) == 0:
            self.getProjectKeys()
        if len( self.projectLeads ) == 0:
            session = self.toSession()
            for pk in self.projectKeys:
                self.projectLeads[ projectKey ] = self.getActiveProjectLead( pk, session )
        return self.projectLeads

    def gatherAllProjectPermissions( self, deletePermissionHelperFile=True ):
        """Function to retrieve project permissions for all projects"""
        if len( self.projectKeys ) == 0:
            self.getProjectKeys()
        if len( self.permissions ) == 0:
            permissionHelperFile = './data/projectPermissionsHelper.json'
            session = self.toSession()
            if not os.path.exists( os.path.dirname( permissionHelperFile ) ):
                os.makedirs( os.path.dirname( permissionHelperFile ), exist_ok=True)
            if not os.path.exists( permissionHelperFile ):
                with open( permissionHelperFile, 'w+'):
                    pass
            with open( permissionHelperFile ) as json_file:
                self.permissions = json.load( json_file )
            for pk in self.projectKeys:
                if pk not in self.permissions:
                    print( pk )
                    self.permissions[ pk ] = self.gatherProjectPermissions( pk, session )
                with open( permissionHelperFile, 'w' ) as json_file:
                        json.dump( self.permissions, json_file )
            print()
            if deletePermissionHelperFile:
                os.remove( permissionHelperFile )
        return self.permissions

    def createGroup( self, groupName ):
        """Create a local user group"""
        groupUrl = self.app[ 'url' ] + '/secure/admin/user/GroupBrowser.jspa'
        self.get( groupUrl )
        field = self.browser.find_element( By.XPATH, '//input[@name="addName"]' )
        field.send_keys( Keys.CONTROL, "a" )
        field.send_keys( groupName )
        field.send_keys( Keys.ENTER )
        session = self.toSession()
        groupCreated = False
        while not groupCreated:
            time.sleep(1)
            rsp = session.get( '{url}rest/api/latest/group?groupname={group}'.format( url=self.app[ 'url' ], group=urllib.parse.quote( groupName ) ) )
            groupCreated = ( rsp.status_code == 200 )


class Confluence ( Atlassian ):
    """Confluence Browser – recommended to use administrative user; otherwise most functions won't work properly"""

    spaceKeys        = []
    spaceNames       = {}
    permissions      = {}
    permissionsNames = []
    appInfo = {
        "url":    {
            "env":         "CONFLUENCE_URL",
            "url":         True,
            "description": "Enter Confluence URL",
        },
        "user":   {
            "env":         "CONFLUENCE_USER",
            "description": "Enter Confluence username",
        },
        "passwd": {
            "password":    True,
            "env":         "CONFLUENCE_PASS",
            "description": "Enter Confluence password",
        },
    }

    def __init__( self ):
        super( Confluence, self ).__init__()

    def login( self, skipSSO=True ):
        """Run Confluence login"""
        loginUrl = self.app[ 'url' ] + "dologin.action"
        if skipSSO:
            loginUrl += '?nosso'
        self.loadCookies( url=loginUrl )
        self.setSessionBaseHeaders()
        userObject = { "os_username": self.app[ 'user' ], "os_password": self.app[ 'passwd' ], "os_cookie": "true", "login": "Log in", "os_destination": "", }
        if os.getenv( "PRINT_DEBUG_INFO", "False" ).lower() in [ "1", "true", "t", "y", "yes" ]:
            print( 'User is being logged in with those credentials:' )
            print( userObject )
            print()
        self.sessionPostRequest( loginUrl, userObject, True, urlOverride=True )
        self.get( self.app[ 'url' ] , False )

    def checkLogin( self ):
        """Check if login is needed"""
        currentUrl = self.browser.current_url
        urlLen     = len( self.app[ 'url' ] )
        if currentUrl[ 0:urlLen ] != self.app[ 'url' ]:
            self.get( self.app[ 'url' ], False )
        try:
            self.browser.find_element( By.ID, 'loginButton' )
            return False
        except:
            return True

    def setSessionBaseHeaders( self, api=False ):
        """Api requests need special headers in Confluence ... sometimes ..."""
        if not api:
            self.sessionBaseHeaders = None
        else:
            self.sessionBaseHeaders = {
                "Content-Type":      "application/json",
                "X-Atlassian-Token": "no-check"
            }

    def getPageInfo( self, spaceKey, title, session=None ):
        """Function to get page information by Confluence space key and page title"""
        self.setSessionBaseHeaders( api=True )
        parameters = {
            'spaceKey': spaceKey,
            'title':    title,
            'expand':   'version,space',
        }
        apiUrl  = '{url}rest/api/content?{params}'.format( url=self.app[ 'url' ], params=urllib.parse.urlencode( parameters ) )
        results = self.apiGetInfo( apiUrl, session=session )
        if results[ 'size' ] > 1:
            raise Exception( 'More than one page found – cannot proceed properly ...' )
        return results[ 'results' ][ 0 ]

    def getPageInfoByID( self, pageID, session=None ):
        """Function to get page information by page ID"""
        self.setSessionBaseHeaders( api=True )
        parameters = {
            'expand':   'version,space',
        }
        apiUrl = '{url}rest/api/content/{id}?{params}'.format( url=self.app[ 'url' ], id=pageID, params=urllib.parse.urlencode( parameters ) )
        result = self.apiGetInfo( apiUrl, session=session )
        return result

    def getSpaceName( self, spaceKey, session=None ):
        """Helper function to retrieve the space name of a Confluence Space"""
        self.setSessionBaseHeaders( api=True )
        apiUrl = '{url}rest/api/space/{spaceKey}'.format( url=self.app[ 'url' ], spaceKey=spaceKey )
        result = self.apiGetInfo( apiUrl, session=session )
        if result != None:
            return result[ 'name' ]

    def getSpaceKeyFromName( self, spaceName, force=False, session=None ):
        """Helper function to retrieve space key by space name"""
        if len( self.spaceNames ) == 0 or force == True:
            sks = self.getSpaceKeys()
            for sk in sks:
                self.spaceNames[ self.getSpaceName( sk ) ] = sk
        if spaceName in self.spaceNames:
            return self.spaceNames[ spaceName ]

    def getSpaceHomepageID( self, spaceKey, session=None ):
        """Helper function to get page ID of homepage of Space"""
        self.setSessionBaseHeaders( api=True )
        parameters = {
            'expand':   'homepage',
            'spaceKey': spaceKey,
        }
        apiUrl = '{url}rest/api/space?{params}'.format( url=self.app[ 'url' ], id=pageID, params=urllib.parse.urlencode( parameters ) )
        result = self.apiGetInfo( apiUrl, session=session )
        if result != None:
            return result[ 'results' ][ 0 ][ 'homepage' ][ 'id' ]

    def createPage( self, title, contentHtml, spaceKey, parent=None, session=None ):
        """helper function to create new pages within Confluence"""
        if parent == None:
            parent = getSpaceHomepageID( spaceKey )

        createUrl    = '{url}rest/api/content'.format( url=self.app[ 'url' ] )
        createObject = {
            "type": "page",
            "title": title,
            "space": {
                "key": spaceKey
            },
            "body": {
                "storage": {
                    "value": contentHtml,
                    "representation": "storage"
                }
            },
            "ancestors": [{
                "id": parent
            }]
        }

        response = self.sessionPostRequest( createUrl, createObject, session )
        rc = response.status_code

        i = 1
        title = createObject[ 'title' ]

        while rc != 200 and 'already exists' in response.json()['message'].lower():
            print( '    ' + response.json()['message'] )
            createObject[ 'title' ] = '{} ({})'.format( title, i )
            response = self.sessionPostRequest( createUrl, createObject, session )
            rc = response.status_code
            i += 1

        if rc == 200:
            return [ response.json()['id'], createObject[ 'title' ] ]
        else:
            raise Exception ( "API Response ({}) was:\n\n{}".format( rc, response.content ) )

    def updatePage( self, newTitle, contentHtml, pageID, spaceKey, version=None, session=None ):
        """helper function to update a pages content"""
        if version == None:
            version = self.getPageInfoByID( pageID )[ 'version' ][ 'number' ] + 1

        createObject = {
            "id": pageID,
            "type": "page",
            "title": newTitle,
            "space": {
                "key": spaceKey
            },
            "body": {
                "storage": {
                    "value": contentHtml,
                    "representation": "storage"
                }
            },
            "version": {
                "number": version
            }
        }

        createUrl = '{url}rest/api/content/{pid}'.format( url=self.app[ 'url' ], pid=pageID )
        response  = self.sessionPutRequest( createUrl, createObject, session=session )
        rc = response.status_code

        if rc == 200:
            return response.json()['id']
        else:
            raise Exception ( "API Response ({}) was:\n\n{}".format( rc, response.content ) )

    def getPageContent( self, pageID, session=None ):
        """helper function to retrieve content of page by pageID"""
        apiUrl = '{url}rest/api/content/{pid}?expand=body.storage'.format( url=self.app[ 'url' ], pid=pid )
        if session == None:
            session = self.toSession( curl = True )
        rspC = session.get( apiUrl )
        if rspC.status_code == 200:
            rsp = json.loads( rspC.text )
            return rsp[ 'body' ][ 'storage' ][ 'value' ]
        else:
            return None


    def deletePage( self, pageID, session=None ):
        """helper function to delete a given page"""
        if session == None:
            session = self.toSession( curl = True )
        rsp = session.delete( '{url}rest/api/content/{id}'.format( url=self.app[ 'url' ], id=pageID ) )
        return rsp

    def getGroups( self ):
        """Retrieve Confluence local groups"""
        cgroups = []
        session = self.toSession()
        stop = False
        i = 0
        while True:
            limit = 1000
            rspC = session.get('{url}rest/api/group?start={start}&limit={limit}'.format( url=self.app[ 'url' ], limit=limit, start=( i * limit ) ) )
            if rspC.status_code == 200:
                rsp = json.loads( rspC.text )
                for g in rsp['results']:
                    cgroups.append( g['name'] )
            else:
                stop = True

            if stop or len( rsp['results'] ) == 0:
                break
            else:
                i += 1
        return cgroups

    def webSudo( self, adjustCookies = True ):
        """run Confluence websudo"""
        authUrl    = '{url}authenticate.action'.format( url=self.app[ 'url' ] )
        sysInfoUrl = '{url}admin/viewgeneralconfig.action'.format( url=self.app[ 'url' ] )
        super( Confluence, self ).webSudo( authUrl, sysInfoUrl, adjustCookies )

    def getSpaceKeys( self, force = False, personalSpaces = False ):
        """get all space keys of Confluence spaces through API"""
        # self.webSudo()
        session = self.toSession( curl=True )
        if force or self.spaceKeys == []:
            self.spaceKeys = []
            stop = False
            i = 0
            users = []
            while True:
                limit = 50
                start = i * limit
                apiUrl = '{url}rest/api/space?start={start}&limit={limit}'.format( url=self.app[ 'url' ], start=start, limit=limit )
                rspJ = session.get( apiUrl )
                if rspJ.status_code == 200:
                    rsp = json.loads( rspJ.text )
                    if rsp[ 'size' ] < limit:
                        stop = True
                    for k in rsp[ 'results' ]:
                        if personalSpaces or k[ 'type' ] not in [ 'personal' ]:
                            self.spaceKeys.append( k[ 'key' ] )
                else:
                    print('start: {s}, limit: {l}, rc: {r}'.format( s=start, l=limit, r=str(rspJ.status_code) ) )
                    stop = True
                if stop or len( rsp['results'] ) == 0:
                    break
                else:
                    i += 1
        return self.spaceKeys

    def getSpaceKeysGUI( self, force=False ):
        """get all space keys of Confluence spaces through GUI"""
        if force or self.spaceKeys == []:
            self.spaceKeys = []
            self.get( self.app[ 'url' ] + 'spacedirectory/view.action' )
            while True:
                soup = self.toSoup()
                self.spaceKeys += [ item[ 'data-spacekey' ] for item in soup.select( 'tbody tr' ) ]
                try:
                    nextBtn = soup.select( '.aui-nav-next a' )[0]
                    check   = nextBtn[ 'href' ]
                    self.browser.find_element( By.XPATH, '//*[contains(concat(" ", normalize-space(@class), " "), " aui-nav-next ")]//a' ).click()
                    time.sleep( 5 )
                except:
                    break
        return self.spaceKeys

    def APIFileRequest( self, url, mime, filename, filecontent, transferCookies = False ):
        """send a file through POST request into space"""
        session = self.toSession( curl=True )
        attachData = {
            "bodyType": "storage",
            "supportedContainerTypes": [
                "space",
                "page"
            ],
                "supportedChildTypes": [
                "attachment",
                "comment"
            ],
            "supportedSpacePermissions": [],
            "preventDuplicateTitle": False,
            "indexing": {
                "enabled": True
            },
            "files": {
                'file': ( filename, filecontent, mime )
            }
        }

        request = session.post( url, data = attachData, headers = { "Content-Type": "multipart/form-data", "X-Atlassian-Token": "no-check" } )
        if transferCookies:
            # write Cookies from POST request to Selenium Browser
            new_cookies = session.cookies.get_dict()
            self.browser.get( request.url )
            for key, value in new_cookies.items():
                self.browser.add_cookie( { "name": key, "value": value } )
            self.get( request.url )
        return request

    def cleanupPermissions( self ):
        """function to clean up permissions in spaces"""
        editPermissionUrl = self.app[ 'url' ] + 'spaces/editspacepermissions.action?edit=Edit+Permissions&key='
        userCheckApiUrl   = self.app[ 'url' ] + 'rest/api/user?username='
        admingroupname    = os.getenv( 'CONFLUENCE_ADMIN_GROUP', 'confluence-administrators' )
        self.getSpaceKeys()
        session = self.toSession()
        resp = session.get( userCheckApiUrl + self.app[ 'user' ] )
        if resp.status_code == 403:
            self.login()
            self.webSudo()
            session = self.toSession()
        for space in self.spaceKeys:
            self.get( editPermissionUrl + space )
            rows         = self.browser.find_elements( By.XPATH, '//*[@id="uPermissionsTable"]//tr')[2:]
            removedUsers = []
            for row in rows:
                username   = row.find_element( By.XPATH,'.//span').text[1:-1]
                userApiUrl = userCheckApiUrl + username
                resp       = session.get( userApiUrl )
                if resp.status_code == 200:
                    # User exists, all fine
                    pass
                elif resp.status_code == 404:
                    removedUsers += [ username ]
                    row.find_element( By.XPATH,'.//td[1]//button').click()
                    # User does not exist, remove all permissions
                else:
                    raise APIError( resp.status_code, userApiUrl )
            time.sleep(4)
            self.browser.find_element( By.XPATH,'//input[@name="save" and @type="submit"]').click()
            time.sleep(2)
            self.get( editPermissionUrl + space )
            rows = self.browser.find_elements( By.XPATH, '//*[@id="uPermissionsTable"]//tr')[2:]
            for row in rows:
                username   = row.find_element( By.XPATH,'.//span').text[1:-1]
                if username in removedUsers:
                    row.find_element( By.XPATH,'.//td[1]//button').click()
            self.browser.find_element( By.XPATH,'//input[@name="save" and @type="submit"]').click()
            time.sleep(2)
            self.get( editPermissionUrl + space )
            rows = self.browser.find_elements( By.XPATH, '//*[@id="uPermissionsTable"]//tr')[2:]
            admins_added = False
            for row in rows:
                username   = row.find_element( By.XPATH,'.//span').text[1:-1]
                if username in removedUsers:
                    if not admins_added:
                        groupaddfield = self.browser.find_element( By.ID,'groups-to-add-autocomplete')
                        groupaddfield.send_keys( Keys.CONTROL, "a" )
                        groupaddfield.send_keys( admingroupname )
                        self.browser.find_element( By.XPATH, '//*[@name="groupsToAddButton" and @type="submit"]' ).click()
                        time.sleep(2)
                        self.browser.find_element( By.XPATH, '//*[@id="gPermissionsTable"]//*[contains(text(), "' + admingroupname + '")]//button' ).click()
                        admins_added = True
                        break
            if admins_added:
                rows = self.browser.find_elements( By.XPATH, '//*[@id="uPermissionsTable"]//tr')[2:]
                for row in rows:
                    username   = row.find_element( By.XPATH,'.//span').text[1:-1]
                    if username in removedUsers:
                        row.find_element( By.XPATH,'.//td[1]//button').click()
            self.browser.find_element( By.XPATH,'//input[@name="save" and @type="submit"]').click()
            time.sleep(2)

    def getPermissionRepresentation( self, boolList, trueVal='X', falseVal='-' ):
        """generate a simple representation of a permission row for Confluence space"""
        rep = ''
        for x in boolList:
            if x:
                rep += trueVal
            else:
                rep += falseVal
        return rep

    def getBoolListFromRepresentation( self, representation, trueVal='X', falseVal='-' ):
        """revert representation of a permission row for Confluence space to boolean list"""
        boolList = []
        for c in representation:
            if c == trueVal:
                boolList.append( True )
            elif c == falseVal:
                boolList.append( False )
            else:
                raise Exception( 'Check your representation – trueVal (\'{trueVal}\') and falseVal (\'{falseVal}\') are not matched by \'{val}\'!'.format( trueVal=trueVal, falseVal=falseVal, val=c ) )
        return boolList

    def getAllSpacePermissions( self, force=False, debug=True ):
        """function to retrieve all space permissions in Confluence"""
        if force or self.permissions == {}:
            self.permissions = {}
            self.getSpaceKeys()
            for space in self.spaceKeys:
                self.permissions[ space ] = self.getSpacePermissions( space )
        return self.permissions

    def getSpacePermissions( self, spaceKey, force=False, debug=False ):
        """function to retrieve space permissions for one Confluence space specified through Space Key"""
        if force or spaceKey not in self.permissions:
            permissionUrl = '{url}spaces/spacepermissions.action?key={space}'.format( url=self.app[ 'url' ], space=spaceKey )
            if debug:
                print( spaceKey )
            self.get( permissionUrl )
            soup = self.toSoup()
            if self.permissionsNames == []:
                mainPerms = [ item.text for item in soup.select('table.permissions tr:first-of-type')[0].find_all('th')[1:] ]
                i = 0
                for item in soup.select('table.permissions tr:nth-of-type(2)')[0].find_all('th')[1:]:
                    try:
                        if 'permissions-group-start' in item[ 'class' ]:
                            i += 1
                    except:
                        pass
                    self.permissionsNames += [ mainPerms[ i ] + ' (' + item.text + ')' ]
            tempPermissions = {}
            anonymous = soup.select('#aPermissionsTable tr:not(:first-of-type):not(:nth-of-type(2))')[0].select( 'td' )
            tempPermissions[ 'ANONYMOUS' ] = { 'anonymous': self.fetchPermissionsFromRow( anonymous[1:] ) }
            users     = soup.select('#uPermissionsTable tr:not(:first-of-type):not(:nth-of-type(2))')
            tempPermissions[ 'USERS' ] = {}
            for row in users:
                tds = row.select( 'td' )
                tempPermissions[ 'USERS' ][ tds[0].select( 'span' )[0].text.strip()[1:-1] ] = self.fetchPermissionsFromRow( tds[1:] )
            groups    = soup.select('#gPermissionsTable tr:not(:first-of-type):not(:nth-of-type(2))')
            tempPermissions[ 'GROUPS' ] = {}
            for row in groups:
                tds = row.select( 'td' )
                tempPermissions[ 'GROUPS' ][ tds[0].text.strip() ] = self.fetchPermissionsFromRow( tds[1:] )
            return tempPermissions
        else:
            return self.permissions[ spaceKey ]

    def fetchPermissionsFromRow( self, row ):
        """helper function to fetch permissions from one table row in permission view of Confluence space"""
        return [ item[ 'data-permission-set' ].lower() != 'false' for item in row ]

    def getGroupMembers( self, group ):
        """Retrieve group member usernames from Confluence"""
        sessionC = self.toSession()
        stop = False
        i = 0
        users = []
        limit = 50
        firstRun = True
        while True:
            parameters = {
                'start': ( i * limit ),
                'limit': limit,
            }
            memberUrl = '{url}rest/api/group/{group}/member?{params}'.format( url=self.app[ 'url' ], group=group, params=urllib.parse.urlencode( parameters ) )
            rspC = sessionC.get( memberUrl )

            if rspC.status_code == 200:
                rsp = json.loads( rspC.text )
                if firstRun and ( rsp[ 'size' ] < rsp[ 'limit' ] or limit != rsp[ 'limit' ] ):
                    limit = rsp[ 'size' ]
                elif rsp[ 'size' ] < limit:
                    stop = True
                for u in rsp['results']:
                    users.append( u[ 'username' ] )
            else:
                print('rc: ' + str(rspC.status_code))
                print(parameters)
                stop = True

            if stop or len( rsp['results'] ) == 0:
                len( rsp['results'] )
                break
            else:
                i += 1
            firstRun = False
        return users

    def getUserApiInfo( self, username, returnResponse=False, session=None ):
        """Function to gather information about a user from API – if `returnResponse` is True, the whole request response is returned, otherwise only the decoded answer object"""
        apiUrl = '{url}rest/mobile/latest/profile/{user}'.format( url=self.app['url'], user=urllib.parse.quote( username ) )
        return self.apiGetInfo( apiUrl, returnResponse, session )

    def recoverConfluencePermissions( self ):
        """Function to recover confluence permissions if a system administrator has no space access. ENSURE YOUR SYSTEM LANGUAGE TO BE ENGLISH!"""
        permsurl = '{url}/admin/permissions/viewdefaultspacepermissions.action'.format( url=self.app['url'] )
        self.browser.get( permsurl )
        xpath = '//a[text()="Recover Permissions"]'
        xpathOk = '//button[text()="OK"]'
        okJS = 'xPathRes = document.evaluate (\'{xpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); xPathRes.singleNodeValue.click();'.format( xpath=xpathOk )
        listOfSpaces = []
        try:
            element = self.browser.find_element( By.XPATH, xpath )
            element.location_once_scrolled_into_view
        except:
            element = False
        while element:
            listOfSpaces += [ element.get_attribute( 'data-space-key' ) ]
            element.click()
            WebDriverWait( self.browser, 10 ).until( EC.presence_of_element_located( ( By.XPATH, xpathOk ) ) )
            self.browser.execute_script( okJS )
            WebDriverWait( self.browser, 10 ).until_not( EC.presence_of_element_located( ( By.ID, 'recover-permissions-dialog' ) ) )
            time.sleep( 0.5 )
            try:
                element = self.browser.find_element( By.XPATH, xpath )
                element.location_once_scrolled_into_view
            except:
                element = False
        return listOfSpaces

    def getAllSpacePermissionsAsRepresentation( self, force=False, debug=True, trueVal='X', falseVal='-' ):
        """
        Function to retrieve dictionary of permission representations.
        First level keys are space keys followed by second key as (like in getAllSpacePermissions) categories `GROUPS`, `USERS` and `ANONYMOUS`.
        The last key-level of the result dictionary is the granted object identifier (group name, user name or `anonymous`) followed by the representation.
        """
        perms = self.getAllSpacePermissions( force, debug )
        vperms = {}
        for spacekey, permissions in perms.items():
            vperms[ spacekey ] = {}
            for category, specificperms in permissions.items():
                vperms[ spacekey ][ category ] = {}
                for key, permarray in specificperms.items():
                    vperms[ spacekey ][ category ][ key ] = self.getPermissionRepresentation( permarray, trueVal, falseVal )
        return vperms

    def addNewSpacePermissions( self, spaceKey, category, objectName, representation, isRepresentation=True, submitChanges=True ):
        """Function to add new space permissions – if `isRepresentation` is `False`, a boolean list for permissions is expected."""
        self.callPermissionChangePage( spaceKey )
        if category == 'GROUPS':
            gfield = self.browser.find_element_by_xpath( '//input[@name="groupsToAdd"]' )
            gfield.send_keys( Keys.CONTROL, "a" )
            gfield.send_keys( objectName )
            time.sleep(1)
            self.browser.find_element( By.XPATH, '//input[@name="groupsToAddButton"]' ).click()
        elif category == 'USERS':
            gfield = self.browser.find_element_by_xpath( '//input[@name="usersToAdd"]' )
            gfield.send_keys( Keys.CONTROL, "a" )
            gfield.send_keys( objectName )
            time.sleep(1)
            self.browser.find_element( By.XPATH, '//input[@name="usersToAddButton"]' ).click()
        elif category == 'ANONYMOUS':
            # ANONYMOUS has only one row which is always present
            pass
        else:
            raise Exception( '{val} is an invalid category!'.format( val=category ) )
        time.sleep(1)
        self.adjustSpacePermissions( spaceKey, category, objectName, representation, isRepresentation, submitChanges )

    def adjustSpacePermissions( self, spaceKey, category, objectName, representation, isRepresentation=True, submitChanges=True ):
        """Function to change existing space permissions – if `isRepresentation` is `False`, a boolean list for permissions is expected."""
        self.callPermissionChangePage( spaceKey )
        if isRepresentation:
            representation = self.getBoolListFromRepresentation( representation )
        try:
            permissionCheckboxes = self.selectObjectRowForSpacePermissionChange( category, objectName, spaceKey )
            if os.getenv( "PRINT_DEBUG_INFO", "False" ).lower() in [ "1", "true", "t", "y", "yes" ]:
                rc  = len( representation )
                pcc = len( permissionCheckboxes )
                if rc != pcc:
                    print( 'Representation length ({rc}) and permission checkboxes lenght ({pcc}) do not match! Values are mapped as far as possible.'.format( rc=rc, pcc=pcc ) )
                    print()
            for i, granted in enumerate( representation ):
                try:
                    element = permissionCheckboxes[ i ].find_element( By.XPATH, './/input[@type="checkbox"]' )
                    while element.is_selected() != granted:
                        element.click()
                except:
                    pass
            if submitChanges:
                self.submitSpacePermissionChange()
        except:
            if os.getenv( "PRINT_DEBUG_INFO", "False" ).lower() in [ "1", "true", "t", "y", "yes" ]:
                print( 'Object {obj} in category {cat} could not be found for space with key {sk} ...'.format( obj=objectName, cat=category, sk=spaceKey ) )

    def removeSpacePermissions( self, spaceKey, category, objectName, submitChanges=True ):
        """Function to remove permissions from space"""
        self.callPermissionChangePage( spaceKey )
        try:
            permissionCheckboxes = self.selectObjectRowForSpacePermissionChange( category, objectName, spaceKey )
            for element in permissionCheckboxes:
                checkbox = element.find_element( By.XPATH, './/input[@type="checkbox"]' )
                while checkbox.is_selected():
                    checkbox.click()
            if submitChanges:
                self.submitSpacePermissionChange()
        except:
            if os.getenv( "PRINT_DEBUG_INFO", "False" ).lower() in [ "1", "true", "t", "y", "yes" ]:
                print( 'Object {obj} in category {cat} could not be found for space with key {sk} ...'.format( obj=objectName, cat=category, sk=spaceKey ) )

    def selectObjectRowForSpacePermissionChange( self, category, objectName, spaceKey ):
        """Helper function to select the correct row for changing permissions"""
        xpathPermissionCell = './/*[contains(concat(" ", normalize-space(@class), " "), " permissionCell ")]'
        if category == 'GROUPS':
            permissionRow = self.browser.find_element( By.XPATH, '//td[@data-permission-group=\'{obj}\'][1]/parent::tr'.format( obj=objectName ) )
        elif category == 'USERS':
            permissionRow = self.browser.find_element( By.XPATH, '//td[@data-permission-user=\'{obj}\'][1]/parent::tr'.format( obj=objectName ) )
        elif category == 'ANONYMOUS':
            permissionRow = self.browser.find_element( By.ID, 'aPermissionsTable' )
            permissionRow = permissionRow.find_element( By.XPATH, '{xpath}[1]/parent::tr'.format( xpath=xpathPermissionCell) )
        else:
            raise Exception( '{val} is an invalid category!'.format( val=category ) )
        permissionCheckboxes = permissionRow.find_elements( By.XPATH, xpathPermissionCell )
        pcc = len( permissionCheckboxes )
        if pcc != 14:
            raise Exception( 'There are {c} permission checkboxes found for object {obj} in space permissions for space with key {sk}! (14 expected ...)'.format( c=pcc, obj=objectName, sk=spaceKey ) )
        return permissionCheckboxes

    def callPermissionChangePage( self, spaceKey ):
        """Helper function to call permission change page for a specified Confluence space"""
        url = '{url}spaces/editspacepermissions.action?key={space}'.format( url=self.app['url'], space=spaceKey )
        if self.browser.current_url != url:
            self.webSudo()
            self.get( url )

    def submitSpacePermissionChange( self ):
        """Submit the permission changes on space permission change page of confluence"""
        time.sleep(1)
        self.browser.find_element( By.XPATH, '//input[@name="save"]' ).click()

    def setSpacePermissions( self, spaceKey, representationDictionary, forceRefresh=False ):
        """Function meant to adjust space permissions to match a representation dictionary like returned by `getAllSpacePermissionsAsRepresentation`."""
        currentPermissions = self.getSpacePermissions( spaceKey, forceRefresh )
        for category in representationDictionary:
            for objectName, newPermissions in representationDictionary[ category ].items():
                if objectName not in currentPermissions[ category ]:
                    self.addNewSpacePermissions( spaceKey, category, objectName, newPermissions, submitChanges=False )
                else:
                    self.adjustSpacePermissions( spaceKey, category, objectName, newPermissions, submitChanges=False )
        # removing permissions has to be the last step since it could be that space permissions then lock out the current user
        for category in representationDictionary:
            for objectName in currentPermissions[ category ]:
                if objectName not in representationDictionary[ category ]:
                    self.removeSpacePermissions( spaceKey, category, objectName, submitChanges=False )
        self.submitSpacePermissionChange()
