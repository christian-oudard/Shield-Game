#! /bin/sh

nosetests --with-coverage \
	--cover-package display \
	--cover-package entity \
	--cover-package keys \
	--cover-package main \
	--cover-package move_shortcuts \
	--cover-package terrain_constants \
	--cover-package test \
	--cover-package world \
