""""
directory_paths.py

Define functions to get common hydrogen directory paths.
"""
import os
import json
import datetime
import logging

def get_hydrodata_directory():
    """Returns the full path of the hydroframe /hydrodata directory containing large files."""
    result = os.environ.get("HYDRODATA", None)
    if not result or not os.path.exists(result):
        # If the HYDRODATA environment variable is not used use default
        result = "/hydrodata"

    return result


def get_hydro_common_directory():
    """Returns the common directory in /home/HYDROAPP/common that contains common static files for all users."""

    # The 'standard' place is different depending upon whether code is running on the client, the VM host or a Docker container
    # It is one of the directories specified by these environment variables
    result = None
    hydrocommon = os.environ.get("HYDROCOMMON", "")
    directory_options = [hydrocommon, "/hydrocommon", "/home/HYDROAPP/common"]
    for dirpath in directory_options:
        if os.path.exists(dirpath):
            result = dirpath
            break
    return result


def get_data_directory():
    """Returns the full path name of the data directory where files are stored, or None if not configured."""

    # The 'standard' place is different depending upon whether code is running on the client, the VM host or a Docker container
    # It is one of the directories specified by these environment variables
    result = None
    directory_env_variables = [
        "CONTAINER_HYDRO_DATA_PATH",
        "CLIENT_HYDRO_DATA_PATH",
        "HOST_HYDRO_DATA_PATH",
    ]
    for env_var in directory_env_variables:
        dirpath = os.environ.get(env_var, None)
        if dirpath is not None and os.path.exists(dirpath):
            result = dirpath
            break
    return result


def get_domain_path(user_id=None, domain_id=None, domain_directory=None, message=None):
    """
    Returns the full path name to the domain directory for the environment where code is running.
    """

    if message is not None:
        user_id = message.get("user_id", None)
        domain_id = message.get("domain_id", None)
        domain_directory = message.get("domain_directory", None)
    if user_id is None:
        raise Exception("No user_id provided.")
    if domain_directory and domain_id is None:
        # For backward compatibility
        domain_id = domain_directory
    if domain_id is None:
        raise Exception("No domain_id provided.")
    domain_id = domain_id.lower()
    user_id = user_id.lower()
    data_dir = get_data_directory()
    domain_path = f"{data_dir}/{user_id}/{domain_id}"
    return domain_path


def get_domain_state(user_id=None, domain_id=None, domain_directory=None, message=None):
    """
    Return the contents of the domain_state.json object of the domain directory.
    """

    result = None
    if message is not None:
        user_id = message.get("user_id", None)
        domain_id = message.get("domain_id", None)
        domain_directory = message.get("domain_directory", None)
    if user_id is None:
        raise Exception("No user_id provided.")
    if domain_directory and domain_id is None:
        # For backward compatibility
        domain_id = domain_directory
    if domain_id is None:
        raise Exception("No domain_id provided.")

    domain_path = get_domain_path(user_id=user_id, domain_id=domain_id)
    domain_state_filename = f"{domain_path}/domain_state.json"
    if os.path.exists(domain_state_filename):
        with open(domain_state_filename, "r") as stream:
            domain_state = stream.read()
            result = json.loads(domain_state)
    # In case the directory was copied or moved put the actual user and directory in the returned state
    if result:
        result["user_id"] = user_id.lower()
        result["domain_id"] = domain_id.lower()
    return result

def update_domain_state(domain_state):
    """
        Update the domain state in the user domain directory with the attributes in the domain_state object.
        The domain_state object must contain at least the 'user_id' and 'domain_id' attributes.
        Other attributes in the object are replaced in the domain state in the user domain directory.
        Attributes not provided in the domain_state object are unchanged in the user domain directory.
    """

    lock_file_name = ""
    try:
        user_id = domain_state.get("user_id", None)
        domain_directory = domain_state.get("domain_directory", None)
        domain_id = domain_state.get("domain_id", None)
        if domain_directory and domain_id is None:
            # For backward compatibility
            domain_id = domain_directory

        if not user_id:
            raise Exception("No user_id in the domain state")
        if not domain_id:
            raise Exception("No domain_id in the domain state")
        domain_path = get_domain_path(user_id=user_id, domain_id=domain_id)
        domain_state_filename = f"{domain_path}/domain_state.json"
        lock_file_name = f"{domain_state_filename}.lck"
        prev_domain_state = {}

        # Create a lock file to protect against two processes writing at the same time
        with open(lock_file_name, "w+") as lock_stream:
            # Lock the lock file before we write the domain_state file
            if not os.name == "nt":
                # fcntl only works on linux so no locking on windows...
                try:
                    import fcntl

                    fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except Exception as e:
                    raise Exception("Domain state was locked. Unable to save") from e

            if os.path.exists(domain_state_filename):
                # Read the previous contents of the prev_domain_state file first
                with open(domain_state_filename, "r") as read_stream:
                    contents = read_stream.read()
                    if contents:
                        prev_domain_state = json.loads(contents)
            with open(domain_state_filename, "w+") as write_stream:
                # Update the attributes from the incoming message, leave the rest alone
                if (
                    prev_domain_state.get("state", None) == "deleted"
                    and prev_domain_state.get("state_before_deleted", None)
                    and domain_state.get("state", None) == "new"
                ):
                    # When un-deleting a domain restore the previous state
                    domain_state["state"] = prev_domain_state.get("state_before_deleted", None)

                # Update values in the new domain_state given the values from in input param
                for attribute_name in domain_state.keys():
                    if not attribute_name in ["user_id", "domain_id", "domain_directory"]:
                        new_value = domain_state.get(attribute_name, None)
                        prev_domain_state[attribute_name] = new_value

                if not prev_domain_state.get("state", None):
                    # If there is no state for the domain then set the state to 'new'
                    prev_domain_state["state"] = "new"
                if not prev_domain_state.get("created_date", None):
                    prev_domain_state["created_date"] = datetime.datetime.utcnow().strftime(
                        "%Y-%m-%dT%H:%M:%S.000Z"
                    )

                # Put the actual user_id and domain_id the prev_domain_state
                prev_domain_state["directory_name"] = domain_id
                prev_domain_state["domain_directory"] = domain_id
                prev_domain_state["user_id"] = user_id
                
                # Save the updated file
                write_stream.write(json.dumps(prev_domain_state, indent=2))
        if os.path.exists(lock_file_name):
            os.remove(lock_file_name)
        return prev_domain_state
    except Exception as e:
        logging.exception("Unable to save domain state")
        if os.path.exists(lock_file_name):
            os.remove(lock_file_name)
        raise Exception("Unable to save domain state") from e


def get_domain_database(message):
    """
    Deprecated!
    Return the contents of the databse.json object of the domain directory.
    Use the user_id and domain_directory values in the message dict.
    This is deprecated. use get_domain_state() instead.
    """

    return get_domain_state(message)


def get_widget(message):
    """
    Deprecated!
    Return the visualization widget from the domain database associated with the
    domain and widget_id defined by the user_id, domain_directory and widget_id from
    the message dict.
    """

    result = None
    widget_id = message.get("widget_id", None)
    database = get_domain_database(message)
    if database is not None:
        for vis_index, vis in enumerate(database.get("visualizations", [])):
            for w_index, w in enumerate(vis.get("widgets", [])):
                if f"{vis_index}.{w_index}" == widget_id:
                    result = w
                    break
            if result:
                break
    return result
