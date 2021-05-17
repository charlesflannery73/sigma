#!/usr/bin/python3

import argparse
import requests
import os
import datetime
import json


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


def search_type():
    verbose("searching for type " + args.type)
    name = "name_like"
    if args.exact:
        name = "name"

    try:
        r = requests.get(url + "/api/v1/type/?" + name + "=" + args.type, headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)


def add_type():
    verbose("adding type " + args.type)
    try:
        data = '{"name":"' + args.type + '", "comment": "' + args.comment + '"}'

        r = requests.post(url + "/api/v1/type/", data, headers=headers)
        if r.status_code == 201:
            print(str(r.text))
        elif r.status_code == 400:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key + " and data " + data)


def delete_type_by_id(type_id):
    verbose("deleting type by id " + type_id)

    verbose("checking if the type has any sigs")
    try:
        r = requests.get(url + "/api/v1/sig/?type_id=" + type_id, headers=headers)
        if r.status_code == 200:
            sigs = json.loads(r.text)
            if sigs:
                verbose("the type has some sigs")
                if args.override:
                    verbose("override is set, lets delete some sigs")
                    for sig in sigs:
                        verbose("deleting " + str(sig["id"]))
                        delete_sig(str(sig["id"]))
                else:
                    print('{"detail": "the type has existing sigs, not deleting anything, use --override or -o if you want to also delete the sigs"}')
                    return
            else:
                verbose("the type has no sigs, safe to delete")
        else:
            verbose("some server issue " + str(r.status_code))
            return
    except:
        verbose("error connecting to server " + url + " with key " + key)
        return

    verbose("made it to here, we either deleted the sigs or there were none")
    try:
        r = requests.delete(url + "/api/v1/type/" + type_id + "/", headers=headers)
        if r.status_code == 204:
            print('{"detail":"delete type id ' + type_id + ' successful"})')
        elif r.status_code == 404:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)

def delete_type_by_text(type_text):
    verbose("deleting type by text " + type_text)

    try:
        r = requests.get(url + "/api/v1/type/?name=" + type_text, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                type_id = str((result[0]["id"]))
                delete_type_by_id(type_id)
            else:
                print('{"detail":"type name ' + type_text + ' not found"})')
    except:
        verbose("error connecting to server " + url + " with key " + key)


def delete_type():
    if args.type.isnumeric():
        delete_type_by_id(args.type)
    else:
        delete_type_by_text(args.type)


def modify_type():
    verbose("modifying type " + args.type)

    # first get the id
    try:
        r = requests.get(url + "/api/v1/type/?name=" + args.type, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                type_id = str((result[0]["id"]))
            else:
                print('{"detail":"type name ' + args.type + ' not found"})')
                return
    except:
        verbose("error connecting to server " + url + " with key " + key)

    # next modify it
    try:
        data = '{"name":"' + args.type + '", "comment": "' + args.comment + '"}'

        r = requests.put(url + "/api/v1/type/" + type_id + "/", data, headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key + " and data " + data)


def generate_type():
    verbose("generating type " + args.generate)
    try:
        r = requests.get(url + "/api/v1/sig/?type=" + args.generate + "&status=" + args.status, headers=headers)
        if r.status_code == 200:
            results = json.loads(r.text)
            for result in results:
                print(result["text"])
    except:
        verbose("error generating type " + args.generate)


def search_sig():
    verbose("searching for sig " + args.sig)
    text = "text_like"
    if args.exact:
        text = "text"

    try:
        r = requests.get(url + "/api/v1/sig/?" + text + "=" + args.sig, headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)


def add_sig():
    verbose("adding sig " + args.sig + " to type " + args.sig_type)

    verbose("first lets get the type id from the type name")
    try:
        r = requests.get(url + "/api/v1/type/?name=" + args.sig_type, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                type_id = (result[0]["id"])
            else:
                verbose("could not find type " + args.sig_type)
                return
        else:
            verbose("some server issue " + str(r.status_code))
            return
    except:
        verbose("error getting type id")

    try:
        data = '{"text":"' + args.sig + '","type":' + str(type_id) + ',"comment":"' + args.comment + '","reference":"' + args.reference + '","expiry":"' + args.expiry + '","status":"' + args.status + '"}'
        verbose(data)
        r = requests.post(url + "/api/v1/sig/", data, headers=headers)
        if r.status_code == 201:
            print(str(r.text))
        elif r.status_code == 400:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key + " and data " + data)


def delete_sig(sig):
    if sig.isnumeric():
        delete_sig_by_id(sig)
    else:
        delete_sig_by_text(sig)


def delete_sig_by_id(sig_id):
    verbose("deleting sig by id " + sig_id)

    try:
        r = requests.delete(url + "/api/v1/sig/" + sig_id + "/", headers=headers)
        if r.status_code == 204:
            print('{"detail":"delete sig id ' + sig_id + ' successful"})')
        elif r.status_code == 404:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error deleting sig by id " + sig_id)


def delete_sig_by_text(sig_text):
    verbose("deleting sig by text " + sig_text)

    try:
        r = requests.get(url + "/api/v1/sig/?text=" + sig_text, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                sig_id = (result[0]["id"])
                delete_sig_by_id(sig_id)
            else:
                verbose("could not find sig " + sig_text)
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error getting type id")


def modify_sig():
    verbose("modifying sig " + args.sig)

    # first get the id
    try:
        r = requests.get(url + "/api/v1/sig/?text=" + args.sig, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                sig_id = str((result[0]["id"]))
            else:
                print('{"detail":"sig name ' + args.sig + ' not found"})')
                return
    except:
        verbose("error connecting to server " + url + " with key " + key)

    # next modify it
    try:
        data = '{"text":"' + args.sig + '","comment":"' + args.comment + '","reference":"' + args.reference + '","expiry":"' + args.expiry + '","status":"' + args.status + '"}'

        r = requests.patch(url + "/api/v1/sig/" + sig_id + "/", data, headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key + " and data " + data)

def dump_all():
    verbose("dumping everything")

    try:
        r = requests.get(url + "/api/v1/type/", headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)

    try:
        r = requests.get(url + "/api/v1/sig/", headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)


if __name__ == "__main__":
    saved_url_file = os.environ['HOME'] + "/.sigma.url"
    saved_api_file = os.environ['HOME'] + "/.sigma.api"

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-u", "--url", metavar='', help="sigma url eg. http://127.0.0.1:8000 or https://sigma.mysite.com or saved in ~.sigma.url")
    parser.add_argument("-k", "--key", metavar='', help="your 40 char apikey - or saved in ~.sigma.api")
    parser.add_argument("-c", "--comment", metavar='', help="a comment", default="")
    parser.add_argument("-x", "--expiry", metavar='', help="the date when the signature is expired - default is now + 3 months", default=str(datetime.date.today() + datetime.timedelta(91)))
    parser.add_argument("-r", "--reference", metavar='', help="a link to a ticket, website or report related to the sig", default="")
    parser.add_argument("--status", metavar='', help="enabled, disabled, testing, pending, expired. default is enabled", default="enabled")
    parser.add_argument("-w", "--sig_type", metavar='', help="the type to use when adding a signature")
    parser.add_argument("-o", "--override", help="by default you can't delete types that have signatures, override will also delete all sigs, then the type", action="store_true")
    parser.add_argument("-e", "--exact", help="by default searching does partial matches, use this flag if you want exact match", action="store_true")

    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("-a", "--add", help="add signature or type", action="store_true")
    operation.add_argument("-d", "--delete", help="delete a signature or type", action="store_true")
    operation.add_argument("-m", "--modify", help="modify a signature or type", action="store_true")
    operation.add_argument("-s", "--search", help="search a signature or type", action="store_true")

    table = parser.add_mutually_exclusive_group()
    table.add_argument("--type", metavar='', help="operate on types")
    table.add_argument("--sig", metavar='', help="operate on signatures")
    table.add_argument("--dump", help="dump all data, types first then sigs", action="store_true")
    table.add_argument("-g", "--generate", metavar='', help="output only the sig text for a given type - no json")

    args = parser.parse_args()

    url = validate_url()
    key = validate_key()

    headers = {'content-type': 'application/json', 'Authorization': 'Token ' + key}

    if args.dump:
        dump_all()

    if args.generate:
        generate_type()

    if args.type:
        if args.search:
            search_type()
        if args.add:
            add_type()
        if args.delete:
            delete_type()
        if args.modify:
            modify_type()


    if args.sig:
        if args.search:
            search_sig()
        if args.add:
            add_sig()
        if args.delete:
            # delete_sig needs to receive an arg because delete_type sends one
            delete_sig(args.sig)
        if args.modify:
            modify_sig()

