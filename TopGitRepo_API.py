# -*- coding: utf-8 -*-
"""
Created on Mon May  6 19:50:21 2019

@author: srjcp
"""

import requests

# Import the framework
from flask import Flask
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)
 
class GetTopRepo(Resource): 
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('org', required=True, help="Organization ID required")
        args = parser.parse_args()
        payload={"sort": 'stars', 'order':'desc'}
        payload['q']= 'org:'+args['org']
        header={'Authorization': 'token AUTH_TOKEN'}##User your auth token
        root='https://api.github.com'
        search_endpoint='/search/repositories'
        rate_endpoint='/rate_limit'
        
        ###Cheching rate limit of Github API
        rate_response=requests.get(url=root+rate_endpoint,headers=header)
        '''Checking if the response is ok or not. If it's ok check our repositories for search endpoint, if not 
           return error message with corresponding status code'''
        if rate_response.ok:    
            resources=rate_response.json()
            remaining_limit=resources['resources']['search']['remaining']
            ##Checking the rate limit of github API. 
            if remaining_limit==0:
                return{'message':'Too many requests. Github API has a rate limit of 30 requests per minute'},429
            else:
                response=requests.get(url=root+search_endpoint,  params=payload, headers=header)
                repositories=response.json()
                if response.ok:     
                    return_response=[]
                    ##Checking if there are any public repositories in an organization
                    if 'items' not in repositories.keys():
                        return {"results": return_response}
                    ##Cheching if there are at least 3 repositories
                    if len(repositories['items'])< 3:
                        for repo in repositories['items'][:len(repositories['items'])]:
                            return_response.append({'name':str(repo['name']),'stars':repo['stargazers_count']})
                    else:
                        for repo in repositories['items'][:3]:
                            return_response.append({'name':str(repo['name']),'stars':repo['stargazers_count']})
                    return{"results": return_response},200
                else:
                    ## Handling the wrong organization name in post request
                    if 'errors' in repositories.keys():
                        return{'message': 'No such orgnization. Please check the orgnization name in post body'},response.status_code
                    else:
                        return{'message':'Bad response from github search repositories endpoint'},response.status_code
        else:
            return{'message':'Bad response from github rate limit endpoint'},rate_response.status_code

api.add_resource(GetTopRepo, '/repo')
if __name__=='__main__':
    app.run(host='localhost', port=8080, debug=True)