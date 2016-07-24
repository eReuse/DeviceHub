"""
    Handles the submission of resources to external agents, like GRD.

    This package is divided in two:
    1. General purpose and extensible classes to handle submission.
    2. An implementation, grd_submitter, which handles submissions to GRD.

    The submission process is as follows:
    - Submitter_caller is instantiated, usually when instantiating DeviceHub, see flaskapp (app.grd_submitter_caller).
    Then:
    1. A hook starts the process by calling 'submit' of a SubmitterCaller instance (app.grd_submitter_caller).
    In grd_submitter, the hook is called after creating an event. The hooks passes the id of the resource.
    2. SubmitterCaller calls Submitter.
    3. Submitter gets the resource using the id, and uses an instance of Translator to transform the resource to fit
    the schema of the other agent. Finally performs log-in (see Auth class) and submits the transformed resource.

    Take a look at grd_submitter for an exemplifying implementation, extending the base Submitter, Translator and Auth
    classes.
"""