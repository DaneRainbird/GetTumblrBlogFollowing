import pytumblr
import json

# Loads credentials from file
def loadCredentials():
    credentials = []
    try:
        file = open('credentials', 'r')
        file = file.read().splitlines()
        for line in file:
            credentials.append(line)

        # There should only ever be four values here, raise an exception otherwise
        if len(credentials) != 4:
            raise Exception("Missing one or more credential values. There should be four keys in the credential file")

        return credentials

    except:
        print("Unable to open or read credential file.\nPlease ensure there is a file named 'credentials' in\nthe current directory that contains all 4 OAuth keys required by Tumblr.")
        return None, None, None, None

# Basic check to see if key variables are set, and if we can authenticate with said values
def checkCredentials(client, consumer_key, consumer_secret, oauth_token, oauth_secret):
    if consumer_key and consumer_secret and oauth_token and oauth_secret:
        try:
            clientAuthDetails = client.info()['user']
            print("Authenticated as {}".format(clientAuthDetails['name']))
            return True
        except:
            print("Failed to validate your credentials with Tumblr. Please ensure your keys are valid and / or inputted.")
            return False
    else:
        return False

# Gets and outputs the names of all the blogs being followed by blogName
def getFollowers(client, blogName, numFollow):
    counter = 0
    while counter < numFollow:
        blogs = callAPI(client, blogName, counter)['blogs'] # grab only the "blogs" key and discard others
        for blog in blogs:
            counter += 1
            print(blog['name'])

    print("Finished pulling followers.")

# Handles the API call. Uses maximum limit value (20), and variable offset value.
def callAPI(client, blogName, offsetVal):
    return client.blog_following(blogName, offset=offsetVal, limit=20)

# Main function
def main(client):
    blogName = input("Enter blog name: ")
    apiReturn = callAPI(client, blogName, 0)

    ''' Presently (06/10/2020), the Tumblr API is a bit weird:
     When you make an API call, there is always a 'meta' key in the return value, such as below:
       "meta": {
           "status": 404,
           "msg": "Not Found"
       },
    For whatever reason, and only for the client.blog_following() function in the Python wrapper,
    there is no meta key if there is a successful call to the API, only for failure.
    As such, I've wrapped this whole thing in a try-catch, to ensure
    that this works even if Tumblr fixes(?) their API responses. '''
    try:
        httpStatus = apiReturn['meta']['status']
        if httpStatus == 403:
            print("That blog has disabled seeing it's followers publicly.")
        elif httpStatus == 404:
            print("That blog doesn't exist.")
        else:
            print("An error occurred.")
        
    except:
        numFollowers = apiReturn['total_blogs']
        print("{} follows {} blogs.\n".format(blogName, numFollowers))
        getFollowers(client, blogName, numFollowers)

def init():
    # Load credentials file
    consumer_key, consumer_secret, oauth_token, oauth_secret = loadCredentials()

    # Set up client
    client = pytumblr.TumblrRestClient(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_secret,
    )
    
    # Run the program
    if checkCredentials(client, consumer_key, consumer_secret, oauth_token, oauth_secret):
        main(client)

if __name__ == "__main__":
    init()
