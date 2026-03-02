"""
Blueprints Package
==================

This package contains Flask Blueprints for modular organization of the Digital Catalyst application.

Blueprint Organization:
- auth: Authentication routes (login, register, logout)
- main: Core application routes (dashboard, heritage sites, artisans, products)
- api: REST API endpoints returning JSON
- dashboard: Analytics and admin dashboard routes

Academic Note:
Blueprints are Flask's mechanism for creating modular, reusable application components.
They allow separation of concerns, making the codebase more maintainable and testable.
Each blueprint can have its own templates, static files, and URL prefix.
"""
