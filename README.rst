Product Data, Tags and Feed
===========================

.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

**This is the Odoo 16 branch.**

**This module is in alpha state. Feel free to provide feedback.**

For advertising partners, product tags, search and website details, you may want to
enrich your products with various data fields and export these.


**Table of contents**

.. contents::
   :local:


Features
--------

This module is especially for you, if you organize colors on product template level,
while size (or other) attributes are handled as a standard Odoo product attributes.

* use sophisticated, reusable data fields to enrich your products with information
* export your data for your advertising partners (only CSV and XLS)
* product data export fields are roughly compatible with the Google Merchant Center Product Data Specification
* group product templates by using an item group with more flexibility than variants
* use flexible color images to present your products
* customize export labels and periodically update your export data
* add product texts and attachments and show them in the product's page
* tag and filter your products


Usage
-----

In your product forms, you find a new tab `Product Data`. Use predefined data fields
like ``Age Group``, ``Condition`` and ``Gender``, and create your own ones like
``Material`` or ``Color``.

Data fields usually have an identifier and a name/content field. The identifier is used
for fixed, not translated values like IDs or export values like ``new``, ``refurbished``
and other values, that are recommended to be exported in English. The name is the
translatable label for users.


Feed
^^^^

To activate the feed, open `Settings` -> `Website`, scroll to the `Product Data`
section and activate the feed.

More details are provided by opening the feed configuration form ``Configure Feed``.
There, you can inspect generated CSV and XLS files, regenerate them and change a couple
of options.

* ``User Context``

The user context will usually be your public user. It will be used to acquire a
pricelist.

* ``Availibility Threshold``

If you want to export your products as out-of-stock when there is less in stock than a
threshold, with this option you can achieve this.

* ``Fields``

Your fields to be exported are specified by a stored standard Odoo export plus a
``Data Export Label``. By default, it confirms to the
`Google Merchant Center Specification`, but is fully customizable.


Item Groups
^^^^^^^^^^^

`Item Groups` offer you an alternative way to handle your variants and their data.
Fields set on an `Item Group` will be automatically set on all related templates, thus,
instead of having to fill in the data for every color you have, you can specify the
common data on the item group.


Tags
^^^^

Currently, the shop tag filter is not yet part of this module. The search by
the ``tags`` parameter works though, for example, when clicking on the tag in the
product view.


Website Product Views
^^^^^^^^^^^^^^^^^^^^^

For a full-featured experience you may want to activate few customizations in your
website product view. Open one product in your shop, and in the `Customize` menu you
find the following options:

* ``Show Product Color Select``

If you organize your product colors on template level as this app is intended, you will
need this custom color select.

* ``Show Product Texts``

Product texts, including the description, are special fields, that can be shown in your
product detail page.

* ``Show Product Tags``

Show the product tags down on the page. This can be helpful to improve your page ranking
in searches, when you use these tags in your export feed. The user can click on a tag
to be redirected to a shop search for this tag.


Pre-Defined Fields
^^^^^^^^^^^^^^^^^^

The select fields ``Gender``, ``Age Groups``, ``Condition`` and
``Google Product Categories`` have pre-defined selectable values. You can change their
names at will, however, it is not recommended to change their identifier.


Additional Fields
^^^^^^^^^^^^^^^^^

There are few additional fields to complement your data model, that are not exported
in default settings.

* ``Line``

The `Line` bundles a range of similar or similarly themed products with different
features and prices. You can use it, to add ``Product Details`` and ``Tags`` that
all associated products have.

* ``Country of Origin``

You country laws or your advertising partners frequently require to indicate the
country of origin of the product.

* ``Other Texts`` and ``Related Documents``

These fields provide you with the possibility to create text descriptions of your data
to be shown as accordion in the product shop page. You can create your own product text
categories, every category corresponds to one accordion headings, while the related
documents are displayed last as downloadable link list.


Limitations
-----------

* There is no shop tag filter view yet. However, it is soon to be added.


Bug Tracker
-----------

Bugs are tracked on `GitHub Issues <https://github.com/ayudoo/ayu_product_data>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/ayudoo/ayu_product_data/issues/new**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
-------

Authors
^^^^^^^

* Michael Jurke
* Ayudoo Ltd <support@ayudoo.bg>
