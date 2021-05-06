#!/usr/bin/python3

import argparse
import requests
import os


def verbose(message):
    if args.verbose:
        print(message)


def validate_url():
    if args.url:
        verbose("checking server reachable " + args.url)
        try:
            r = requests.get(args.url + "/api/")
            if r.status_code==200:
                verbose("server api is ok " + str(r.status_code))
            else:
                verbose("some server issue " + str(r.status_code))
                exit(1)
        except:
            verbose("error connecting to server " + args.url)
            exit(1)
        try:
            f = open(saved_url_file, "w")
            f.write(args.url)
            f.close()
        except:
            verbose("error saving url to " + saved_url_file)
        return args.url
    else:
        verbose("no url given, checking for a saved one in " + saved_url_file)
        try:
            f = open(saved_url_file, "r")
            url = f.read()
        except:
            verbose("error finding saved url file - please provide a url with the -u option")
            exit(1)
        try:
            r = requests.get(url + "/api/")
            if r.status_code==200:
                verbose(url + " server api is ok " + str(r.status_code))
                return url
            else:
                verbose(url + " some server issue " + str(r.status_code))
                exit(1)
        except:
            verbose("error connecting to server " + url)
            exit(1)


def validate_key():
    if args.key:
        verbose("checking apikey " + args.key)
        try:
            headers = {'content-type': 'application/json', 'Authorization': 'Token ' + args.key}
            r = requests.get(url + "/api/v1/sig/", headers=headers)
            if r.status_code == 200:
                verbose("api key is ok " + str(r.status_code))
            else:
                verbose("some server issue " + str(r.status_code))
                exit(1)
        except:
            verbose("error connecting to server " + args.key)
            exit(1)
        try:
            f = open(saved_api_file, "w")
            f.write(args.key)
            f.close()
        except:
            verbose("error saving apikey to " + saved_api_file)
        return args.api
    else:
        verbose("no apikey given, checking for a saved one in " + saved_api_file)
        try:
            f = open(saved_api_file, "r")
            key = f.read()
        except:
            verbose("error finding saved api file - please provide a api with the -a option")
            exit(1)
        try:
            headers = {'content-type': 'application/json', 'Authorization': 'Token ' + key}
            r = requests.get(url + "/api/v1/sig/", headers=headers)
            if r.status_code == 200:
                verbose("api key is ok " + str(r.status_code))
            else:
                verbose("some server issue " + str(r.status_code))
                exit(1)
        except:
            verbose("error connecting to server " + url)
            exit(1)
        return key


def search_type(type):
    verbose("searching for type " + type)


def search_sig(sig):
    verbose("searching for sig " + sig)


def add_type(type):
    verbose("adding type " + type)


def add_sig(sig):
    verbose("adding sig " + sig)


if __name__ == "__main__":
    saved_url_file = os.environ['HOME'] + "/.sigma.url"
    saved_api_file = os.environ['HOME'] + "/.sigma.api"

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-u", "--url", metavar='', help="sigma url eg. http://127.0.0.1:8000 or https://sigma.mysite.com")
    parser.add_argument("-k", "--key", metavar='', help="your 40 char apikey")
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("-a", "--add", help="add signature or type", action="store_true")
    operation.add_argument("-d", "--delete", help="delete a signature or type", action="store_true")
    operation.add_argument("-m", "--modify", help="modify a signature or type", action="store_true")
    operation.add_argument("-s", "--search", help="search a signature or type", action="store_true")
    table = parser.add_mutually_exclusive_group()
    table.add_argument("--type", metavar='', help="operate on types")
    table.add_argument("--sig", metavar='', help="operate on signatures")
    args = parser.parse_args()

    url = validate_url()
    key = validate_key()

    if args.search:
        if args.type:
            search_type(args.type)
        if args.sig:
            search_sig(args.sig)

    if args.add:
        if args.type:
            add_type(args.type)
        if args.sig:
            add_sig(args.sig)
