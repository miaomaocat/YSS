# -*- coding: utf-8 -*-
from yss import app
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

from yss.model.Content import *
from yss.model.Chapter import *
from yss.model.Collection import *

try:
    import simplejson as json
except ImportError:
    import json
