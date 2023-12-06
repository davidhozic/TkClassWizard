=================================
Missing annotations
=================================

When we are defining our own objects, we can always annotate them and allow TkClassWizard to work without
any problems.
Unfortunately other (including Python's built-in) libraries may not have types annotated inside their classes and functions.
If we wish to use those libraries and graphically define objects with TkClassWizard, we will have problems.

To solve the issue of missing annotations, TkClassWizard contains an annotations module for dealing with missing
annotations.

