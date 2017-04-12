# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:07:12 2017

@author: U6038155
"""

from django.template import Context, Template


t = Template('My name is {{ name }}.')
c = Context({'name': 'Stephane'})
t.render(c)