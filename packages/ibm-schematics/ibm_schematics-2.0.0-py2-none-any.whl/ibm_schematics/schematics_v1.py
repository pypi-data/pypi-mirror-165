# coding: utf-8

# (C) Copyright IBM Corp. 2021.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# IBM OpenAPI SDK Code Generator Version: 3.37.0-a85661cd-20210802-190136
 
"""
IBM Cloud Schematics service is to provide the capability to manage resources  of cloud
provider infrastructure by using file based configurations.  With the IBM Cloud Schematics
service you can specify the  required set of resources and the configuration in `config
files`,  and then pass the config files to the service to fulfill it by  calling the
necessary actions on the infrastructure.  This principle is known as Infrastructure as
Code.  For more information, refer to [Getting started with IBM Cloud Schematics]
(https://cloud.ibm.com/docs/schematics?topic=schematics-getting-started).
"""

from datetime import datetime
from enum import Enum
from typing import BinaryIO, Dict, List
import base64
import json

from ibm_cloud_sdk_core import BaseService, DetailedResponse
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
from ibm_cloud_sdk_core.utils import convert_model, datetime_to_string, string_to_datetime

from .common import get_sdk_headers

##############################################################################
# Service
##############################################################################

class SchematicsV1(BaseService):
    """The schematics V1 service."""

    DEFAULT_SERVICE_URL = 'https://schematics-dev.containers.appdomain.cloud'
    DEFAULT_SERVICE_NAME = 'schematics'

    @classmethod
    def new_instance(cls,
                     service_name: str = DEFAULT_SERVICE_NAME,
                    ) -> 'SchematicsV1':
        """
        Return a new client for the schematics service using the specified
               parameters and external configuration.
        """
        authenticator = get_authenticator_from_environment(service_name)
        service = cls(
            authenticator
            )
        service.configure_service(service_name)
        return service

    def __init__(self,
                 authenticator: Authenticator = None,
                ) -> None:
        """
        Construct a new client for the schematics service.

        :param Authenticator authenticator: The authenticator specifies the authentication mechanism.
               Get up to date information from https://github.com/IBM/python-sdk-core/blob/master/README.md
               about initializing the authenticator of your choice.
        """
        BaseService.__init__(self,
                             service_url=self.DEFAULT_SERVICE_URL,
                             authenticator=authenticator)


    #########################
    # util
    #########################


    def list_schematics_location(self,
        **kwargs
    ) -> DetailedResponse:
        """
        List supported schematics locations.

        Retrieve a list of IBM Cloud locations where you can create Schematics workspaces.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[SchematicsLocations]` result
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_schematics_location')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/locations'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def list_locations(self,
        **kwargs
    ) -> DetailedResponse:
        """
        List supported schematics locations.

        Retrieve a list of IBM Cloud locations where you can work with Schematics objects.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `SchematicsLocationsList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_locations')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/locations'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def list_resource_group(self,
        **kwargs
    ) -> DetailedResponse:
        """
        List resource groups.

        Retrieve a list of IBM Cloud resource groups that your account has access to.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[ResourceGroupResponse]` result
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_resource_group')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/resource_groups'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_schematics_version(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Get Schematics API information.

        Retrieve detailed information about the IBM Cloud Schematics API version and the
        version of the provider plug-ins that the API uses.
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to the workspace ID and the resource group. For more
        information, about Schematics access and permissions, see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `VersionResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_schematics_version')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/version'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def process_template_meta_data(self,
        template_type: str,
        source: 'ExternalSource',
        *,
        region: str = None,
        source_type: str = None,
        x_github_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create metadata by  processing the template.

        Create a Template metadata definition.

        :param str template_type: Template type (terraform, ansible, helm,
               cloudpak, bash script).
        :param ExternalSource source: Source of templates, playbooks, or controls.
        :param str region: (optional) Region to which request should go. Applicable
               only on global endpoint.
        :param str source_type: (optional) Type of source for the Template.
        :param str x_github_token: (optional) The personal access token to
               authenticate with your private GitHub or GitLab repository and access your
               Terraform template.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateMetaDataResponse` object
        """

        if template_type is None:
            raise ValueError('template_type must be provided')
        if source is None:
            raise ValueError('source must be provided')
        source = convert_model(source)
        headers = {
            'X-Github-token': x_github_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='process_template_meta_data')
        headers.update(sdk_headers)

        data = {
            'template_type': template_type,
            'source': source,
            'region': region,
            'source_type': source_type
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/template_metadata_processor'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response

    #########################
    # workspaces
    #########################


    def list_workspaces(self,
        *,
        offset: int = None,
        limit: int = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List workspaces.

        Retrieve a list of Schematics workspaces from your IBM Cloud account that you have
        access to. The list of workspaces that is returned depends on the API endpoint
        that you use. For example, if you use an API endpoint for a geography, such as
        North America, only workspaces that are created in `us-south` or `us-east` are
        returned. For more information about supported API endpoints, see [API
        endpoints](/apidocs/schematics#api-endpoints).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to the workspace ID and the resource group. For more
        information, about Schematics access and permissions, see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param int offset: (optional) The starting position of the item in the list
               of items. For example, if you have three workspaces in your account, the
               first workspace is assigned position number 0, the second workspace is
               assigned position number 1, and so forth. If you have 6 workspaces and you
               want to list the details for workspaces 2-6, enter 1. To limit the number
               of workspaces that is returned, use the `limit` option in addition to the
               `offset` option. Negative numbers are not supported and are ignored.
        :param int limit: (optional) The maximum number of items that you want to
               list. The number must be a positive integer between 1 and 2000. If no value
               is provided, 100 is used by default.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponseList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_workspaces')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/workspaces'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def create_workspace(self,
        *,
        applied_shareddata_ids: List[str] = None,
        catalog_ref: 'CatalogRef' = None,
        description: str = None,
        location: str = None,
        name: str = None,
        resource_group: str = None,
        shared_data: 'SharedTargetData' = None,
        tags: List[str] = None,
        template_data: List['TemplateSourceDataRequest'] = None,
        template_ref: str = None,
        template_repo: 'TemplateRepoRequest' = None,
        type: List[str] = None,
        workspace_status: 'WorkspaceStatusRequest' = None,
        x_github_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a workspace.

        Create an IBM Cloud Schematics workspace that points to the source repository
        where your Terraform template or the IBM Cloud software template is stored. You
        can decide to create your workspace without connecting it to a GitHub or GitLab
        repository. Your workspace is then created with a **Draft** state. To later
        connect your workspace to a GitHub or GitLab repository, you must use the `PUT
        /v1/workspaces/{id}` API to update the workspace or use the
        `/v1/workspaces/{id}/templates/{template_id}/template_repo_upload` API to upload a
        TAR file instead.
         **Getting API endpoint**:-
         * The Schematics API endpoint that you use to create the workspace determines
        where your Schematics actions run and your data is stored. See [API
        endpoints](/apidocs/schematics#api-endpoints) for more information.
         * If you use the API endpoint for a geography and not a specific location, such
        as North America, you can specify the location in your API request body.
         * If you do not specify the location in the request body, Schematics determines
        your workspace location based on availability.
         * If you use an API endpoint for a specific location, such as Frankfurt, the
        location that you enter in your API request body must match your API endpoint.
         * You also have the option to not specify a location in your API request body if
        you use a location-specific API endpoint.
         **Getting IAM access token** :-
         * Before you create Schematics workspace, you need to create the IAM access token
        for your IBM Cloud Account.
         * To create IAM access token, use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`
        and execute `curl -X POST "https://iam.cloud.ibm.com/identity/token" -H
        "Content-Type= application/x-www-form-urlencoded" -d
        "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY" -u
        bx:bx`. For more information, about creating IAM access token and API Docs, see
        [IAM access token](/apidocs/iam-identity-token-api#gettoken-password) and [Create
        API key](/apidocs/iam-identity-token-api#create-api-key).
         * You can set the environment values  `export ACCESS_TOKEN=<access_token>` and
        `export REFRESH_TOKEN=<refresh_token>`.
         * You can use the obtained IAM access token in create workspace `curl` command.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access
         to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param List[str] applied_shareddata_ids: (optional) List of applied shared
               dataset ID.
        :param CatalogRef catalog_ref: (optional) Information about the software
               template that you chose from the IBM Cloud catalog. This information is
               returned for IBM Cloud catalog offerings only.
        :param str description: (optional) The description of the workspace.
        :param str location: (optional) The location where you want to create your
               Schematics workspace and run the Schematics jobs. The location that you
               enter must match the API endpoint that you use. For example, if you use the
               Frankfurt API endpoint, you must specify `eu-de` as your location. If you
               use an API endpoint for a geography and you do not specify a location,
               Schematics determines the location based on availability.
        :param str name: (optional) The name of your workspace. The name can be up
               to 128 characters long and can include alphanumeric characters, spaces,
               dashes, and underscores. When you create a workspace for your own Terraform
               template, consider including the microservice component that you set up
               with your Terraform template and the IBM Cloud environment where you want
               to deploy your resources in your name.
        :param str resource_group: (optional) The ID of the resource group where
               you want to provision the workspace.
        :param SharedTargetData shared_data: (optional) Information about the
               Target used by the templates originating from the  IBM Cloud catalog
               offerings. This information is not relevant for workspace created using
               your own Terraform template.
        :param List[str] tags: (optional) A list of tags that are associated with
               the workspace.
        :param List[TemplateSourceDataRequest] template_data: (optional) Input data
               for the Template.
        :param str template_ref: (optional) Workspace template ref.
        :param TemplateRepoRequest template_repo: (optional) Input variables for
               the Template repoository, while creating a workspace.
        :param List[str] type: (optional) List of Workspace type.
        :param WorkspaceStatusRequest workspace_status: (optional)
               WorkspaceStatusRequest -.
        :param str x_github_token: (optional) The personal access token to
               authenticate with your private GitHub or GitLab repository and access your
               Terraform template.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponse` object
        """

        if catalog_ref is not None:
            catalog_ref = convert_model(catalog_ref)
        if shared_data is not None:
            shared_data = convert_model(shared_data)
        if template_data is not None:
            template_data = [convert_model(x) for x in template_data]
        if template_repo is not None:
            template_repo = convert_model(template_repo)
        if workspace_status is not None:
            workspace_status = convert_model(workspace_status)
        headers = {
            'X-Github-token': x_github_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_workspace')
        headers.update(sdk_headers)

        data = {
            'applied_shareddata_ids': applied_shareddata_ids,
            'catalog_ref': catalog_ref,
            'description': description,
            'location': location,
            'name': name,
            'resource_group': resource_group,
            'shared_data': shared_data,
            'tags': tags,
            'template_data': template_data,
            'template_ref': template_ref,
            'template_repo': template_repo,
            'type': type,
            'workspace_status': workspace_status
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/workspaces'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def get_workspace(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get workspace details.

        Retrieve detailed information for a workspace in your IBM Cloud account.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
         access to the workspace ID and the resource group. For more information,
         about Schematics access and permissions, see [Schematics service access
         roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def replace_workspace(self,
        w_id: str,
        *,
        catalog_ref: 'CatalogRef' = None,
        description: str = None,
        name: str = None,
        shared_data: 'SharedTargetData' = None,
        tags: List[str] = None,
        template_data: List['TemplateSourceDataRequest'] = None,
        template_repo: 'TemplateRepoUpdateRequest' = None,
        type: List[str] = None,
        workspace_status: 'WorkspaceStatusUpdateRequest' = None,
        workspace_status_msg: 'WorkspaceStatusMessage' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update workspace.

        Use this API to update or replace the entire workspace, including the Terraform
        template (`template_repo`) or IBM Cloud catalog software template (`catalog_ref`)
        that your workspace points to.
         **Tip**:- If you want to update workspace metadata, use the `PATCH
        /v1/workspaces/{id}` API.
         To update workspace variables, use the `PUT
        /v1/workspaces/{id}/template_data/{template_id}/values` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param CatalogRef catalog_ref: (optional) Information about the software
               template that you chose from the IBM Cloud catalog. This information is
               returned for IBM Cloud catalog offerings only.
        :param str description: (optional) The description of the workspace.
        :param str name: (optional) The name of the workspace.
        :param SharedTargetData shared_data: (optional) Information about the
               Target used by the templates originating from the  IBM Cloud catalog
               offerings. This information is not relevant for workspace created using
               your own Terraform template.
        :param List[str] tags: (optional) A list of tags that you want to associate
               with your workspace.
        :param List[TemplateSourceDataRequest] template_data: (optional) Input data
               for the Template.
        :param TemplateRepoUpdateRequest template_repo: (optional) Input to update
               the template repository data.
        :param List[str] type: (optional) List of Workspace type.
        :param WorkspaceStatusUpdateRequest workspace_status: (optional) Input to
               update the workspace status.
        :param WorkspaceStatusMessage workspace_status_msg: (optional) Information
               about the last job that ran against the workspace. -.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if catalog_ref is not None:
            catalog_ref = convert_model(catalog_ref)
        if shared_data is not None:
            shared_data = convert_model(shared_data)
        if template_data is not None:
            template_data = [convert_model(x) for x in template_data]
        if template_repo is not None:
            template_repo = convert_model(template_repo)
        if workspace_status is not None:
            workspace_status = convert_model(workspace_status)
        if workspace_status_msg is not None:
            workspace_status_msg = convert_model(workspace_status_msg)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_workspace')
        headers.update(sdk_headers)

        data = {
            'catalog_ref': catalog_ref,
            'description': description,
            'name': name,
            'shared_data': shared_data,
            'tags': tags,
            'template_data': template_data,
            'template_repo': template_repo,
            'type': type,
            'workspace_status': workspace_status,
            'workspace_status_msg': workspace_status_msg
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def delete_workspace(self,
        refresh_token: str,
        w_id: str,
        *,
        destroy_resources: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete a workspace.

        Deletes a workspace from IBM Cloud Schematics. Deleting a workspace does not
        automatically remove the IBM Cloud resources that the workspace manages. To remove
        all resources that are associated with the workspace, use the `DELETE
        /v1/workspaces/{id}?destroy_resources=true` API.
         **Note**: If you delete a workspace without deleting the resources,
         you must manage your resources with the resource dashboard or CLI afterwards.
         You cannot use IBM Cloud Schematics anymore to manage your resources.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access
         to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str refresh_token: The IAM refresh token for the user or service
               identity. The IAM refresh token is required only if you want to destroy the
               Terraform resources before deleting the Schematics workspace. If you want
               to delete the workspace only and keep all your Terraform resources, refresh
               token is not required.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str destroy_resources: (optional) If set to `true`, refresh_token
               header configuration is required to delete all the Terraform resources, and
               the Schematics workspace. If set to `false`, you can remove only the
               workspace. Your Terraform resources are still available and must be managed
               with the resource dashboard or CLI.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `str` result
        """

        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_workspace')
        headers.update(sdk_headers)

        params = {
            'destroy_resources': destroy_resources
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def update_workspace(self,
        w_id: str,
        *,
        catalog_ref: 'CatalogRef' = None,
        description: str = None,
        name: str = None,
        shared_data: 'SharedTargetData' = None,
        tags: List[str] = None,
        template_data: List['TemplateSourceDataRequest'] = None,
        template_repo: 'TemplateRepoUpdateRequest' = None,
        type: List[str] = None,
        workspace_status: 'WorkspaceStatusUpdateRequest' = None,
        workspace_status_msg: 'WorkspaceStatusMessage' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update workspace metadata.

        Use this API to update the following workspace metadata:
         * Workspace name (`name`) - **Note**: Updating the workspace name does not update
        the ID of the workspace.
         * Workspace description (`description`)
         * Tags (`tags[]`)
         * Resource group (`resource_group`)
         * Workspace status (`workspace_status.frozen`)
         **Tip**: If you want to update information about the Terraform template
         or IBM Cloud catalog software template that your workspace points to,
         use the `PUT /v1/workspaces/{id}` API. To update workspace variables,
         use the `PUT /v1/workspaces/{id}/template_data/{template_id}/values` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param CatalogRef catalog_ref: (optional) Information about the software
               template that you chose from the IBM Cloud catalog. This information is
               returned for IBM Cloud catalog offerings only.
        :param str description: (optional) The description of the workspace.
        :param str name: (optional) The name of the workspace.
        :param SharedTargetData shared_data: (optional) Information about the
               Target used by the templates originating from the  IBM Cloud catalog
               offerings. This information is not relevant for workspace created using
               your own Terraform template.
        :param List[str] tags: (optional) A list of tags that you want to associate
               with your workspace.
        :param List[TemplateSourceDataRequest] template_data: (optional) Input data
               for the Template.
        :param TemplateRepoUpdateRequest template_repo: (optional) Input to update
               the template repository data.
        :param List[str] type: (optional) List of Workspace type.
        :param WorkspaceStatusUpdateRequest workspace_status: (optional) Input to
               update the workspace status.
        :param WorkspaceStatusMessage workspace_status_msg: (optional) Information
               about the last job that ran against the workspace. -.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if catalog_ref is not None:
            catalog_ref = convert_model(catalog_ref)
        if shared_data is not None:
            shared_data = convert_model(shared_data)
        if template_data is not None:
            template_data = [convert_model(x) for x in template_data]
        if template_repo is not None:
            template_repo = convert_model(template_repo)
        if workspace_status is not None:
            workspace_status = convert_model(workspace_status)
        if workspace_status_msg is not None:
            workspace_status_msg = convert_model(workspace_status_msg)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_workspace')
        headers.update(sdk_headers)

        data = {
            'catalog_ref': catalog_ref,
            'description': description,
            'name': name,
            'shared_data': shared_data,
            'tags': tags,
            'template_data': template_data,
            'template_repo': template_repo,
            'type': type,
            'workspace_status': workspace_status,
            'workspace_status_msg': workspace_status_msg
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PATCH',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_readme(self,
        w_id: str,
        *,
        ref: str = None,
        formatted: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Show workspace template readme.

        Retrieve the `README.md` file of the Terraform of IBM Cloud catalog template that
        your workspace points to.

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str ref: (optional) The GitHub or GitLab branch where the
               `README.md` file is stored,  or the commit ID or tag that references the
               `README.md` file that you want to retrieve.  If you do not specify this
               option, the `README.md` file is retrieved from the master branch by
               default.
        :param str formatted: (optional) The format of the readme file.  Value
               ''markdown'' will give markdown, otherwise html.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateReadme` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_readme')
        headers.update(sdk_headers)

        params = {
            'ref': ref,
            'formatted': formatted
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/templates/readme'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def template_repo_upload(self,
        w_id: str,
        t_id: str,
        *,
        file: BinaryIO = None,
        file_content_type: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Upload a TAR file to your workspace.

        Provide your Terraform template by uploading a TAR file from your local machine.
        Before you use this API, you must create a workspace without a link to a GitHub or
        GitLab repository with the `POST /v1/workspaces` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access to the workspace ID and the resource group. For more information, about
        Schematics access and permissions, see [Schematics service access roles and
        required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace where you want to upload your
               `.tar` file. To find the workspace ID, use the `GET /v1/workspaces` API.
        :param str t_id: The ID of the Terraform template in your workspace. When
               you create a workspace, a unique ID is assigned to your Terraform template,
               even if no template was provided during workspace creation. To find this
               ID, use the `GET /v1/workspaces` API and review the `template_data.id`
               value.
        :param BinaryIO file: (optional) Template tar file.
        :param str file_content_type: (optional) The content type of file.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateRepoTarUploadResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='template_repo_upload')
        headers.update(sdk_headers)

        form_data = []
        if file:
            form_data.append(('file', (None, file, file_content_type or 'application/octet-stream')))

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/template_data/{t_id}/template_repo_upload'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       files=form_data)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_inputs(self,
        w_id: str,
        t_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        List workspace input variables.

        Retrieve a list of input variables that are declared in your Terraform or IBM
        Cloud catalog template.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str t_id: The ID of the Terraform template in your workspace.  When
               you create a workspace, the Terraform template that  your workspace points
               to is assigned a unique ID. Use the `GET /v1/workspaces` to look up the
               workspace IDs  and template IDs or `template_data.id` in your IBM Cloud
               account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateValues` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_inputs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/template_data/{t_id}/values'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def replace_workspace_inputs(self,
        w_id: str,
        t_id: str,
        *,
        env_values: List[object] = None,
        values: str = None,
        variablestore: List['WorkspaceVariableRequest'] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace workspace input variables.

        Replace or Update the input variables for the template that your workspace points
        to.

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str t_id: The ID of the Terraform template in your workspace.  When
               you create a workspace, the Terraform template that  your workspace points
               to is assigned a unique ID. Use the `GET /v1/workspaces` to look up the
               workspace IDs  and template IDs or `template_data.id` in your IBM Cloud
               account.
        :param List[object] env_values: (optional) A list of environment variables
               that you want to apply during the execution of a bash script or Terraform
               job. This field must be provided as a list of key-value pairs, for example,
               **TF_LOG=debug**. Each entry will be a map with one entry where `key is the
               environment variable name and value is value`. You can define environment
               variables for IBM Cloud catalog offerings that are provisioned by using a
               bash script. See [example to use special environment
               variable](https://cloud.ibm.com/docs/schematics?topic=schematics-set-parallelism#parallelism-example)
                that are supported by Schematics.
        :param str values: (optional) User values.
        :param List[WorkspaceVariableRequest] variablestore: (optional)
               VariablesRequest -.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `UserValues` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        if variablestore is not None:
            variablestore = [convert_model(x) for x in variablestore]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_workspace_inputs')
        headers.update(sdk_headers)

        data = {
            'env_values': env_values,
            'values': values,
            'variablestore': variablestore
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/template_data/{t_id}/values'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def get_all_workspace_inputs(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get workspace template details.

        Retrieve detailed information about the Terraform template that your workspace
        points to.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
         access to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace for which you want to retrieve
               input parameters and  values. To find the workspace ID, use the `GET
               /workspaces` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceTemplateValuesResponse` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_all_workspace_inputs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/templates/values'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_input_metadata(self,
        w_id: str,
        t_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        List workspace variable metadata.

        Retrieve the metadata for all the workspace input variables that are declared in
        the template that your workspace points to.

        :param str w_id: The ID of the workspace for which you want to retrieve the
               metadata of the input variables that are declared in the template. To find
               the workspace ID, use the `GET /v1/workspaces` API.
        :param str t_id: The ID of the Terraform template for which you want to
               retrieve the metadata of your input variables. When you create a workspace,
               the Terraform template that your workspace points to is assigned a unique
               ID. To find this ID, use the `GET /v1/workspaces` API and review the
               `template_data.id` value.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[object]` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_input_metadata')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/template_data/{t_id}/values_metadata'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_outputs(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        List workspace output values.

        Retrieve a list of Terraform output variables. You define output values in your
        Terraform template to include information that you want to make accessible for
        other Terraform templates.

        :param str w_id: The ID of the workspace for which you want to retrieve
               output parameters and  values. To find the workspace ID, use the `GET
               /workspaces` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[OutputValuesInner]` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_outputs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/output_values'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_resources(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        List workspace resources.

        Retrieve a list of IBM Cloud resources that you created with your workspace.

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[TemplateResources]` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_resources')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/resources'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_state(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get Terraform statefile URL.

        Retrieve the URL to the Terraform statefile (`terraform.tfstate`). You use the URL
        to access the Terraform statefile. The Terraform statefile includes detailed
        information about the IBM Cloud resources that you provisioned with IBM Cloud
        Schematics and Schematics uses the file to determine future create, modify, or
        delete actions for your resources. To show the content of the Terraform statefile,
        use the `GET /v1/workspaces/{id}/runtime_data/{template_id}/state_store` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access
         to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace for which you want to retrieve the
               Terraform statefile.  To find the workspace ID, use the `GET
               /v1/workspaces` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `StateStoreResponseList` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_state')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/state_stores'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_template_state(self,
        w_id: str,
        t_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Show Terraform statefile content.

        Show the content of the Terraform statefile (`terraform.tfstate`) that was created
        when your Terraform template was applied in IBM Cloud. The statefile holds
        detailed information about the IBM Cloud resources that were created by IBM Cloud
        Schematics and Schematics uses the file to determine future create, modify, or
        delete actions for your resources.

        :param str w_id: The ID of the workspace for which you want to retrieve the
               Terraform statefile.  To find the workspace ID, use the `GET
               /v1/workspaces` API.
        :param str t_id: The ID of the Terraform template for which you want to
               retrieve the Terraform statefile.  When you create a workspace, the
               Terraform template that your workspace points to is assigned a unique ID.
               To find this ID, use the `GET /v1/workspaces` API and review the
               template_data.id value.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[object]` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_template_state')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/runtime_data/{t_id}/state_store'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_activity_logs(self,
        w_id: str,
        activity_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get workspace job log URL.

        Get the Terraform log file URL for a workspace job. You can retrieve the log URL
        for jobs that were created with the `PUT /v1/workspaces/{id}/apply`, `POST
        /v1/workspaces/{id}/plan`, or `DELETE /v1/workspaces/{id}/destroy` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access
         to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace for which you want to retrieve the
               Terraform statefile.  To find the workspace ID, use the `GET
               /v1/workspaces` API.
        :param str activity_id: The ID of the activity or job, for which you want
               to retrieve details.  To find the job ID, use the `GET
               /v1/workspaces/{id}/actions` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityLogs` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if activity_id is None:
            raise ValueError('activity_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_activity_logs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 'activity_id']
        path_param_values = self.encode_path_vars(w_id, activity_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/actions/{activity_id}/logs'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_log_urls(self,
        w_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get latest workspace job log URL for all workspace templates.

        Retrieve the log file URL for the latest job of a template that ran against your
        workspace. You use this URL to retrieve detailed logs for the latest job.

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `LogStoreResponseList` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_log_urls')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/log_stores'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def get_template_logs(self,
        w_id: str,
        t_id: str,
        *,
        log_tf_cmd: bool = None,
        log_tf_prefix: bool = None,
        log_tf_null_resource: bool = None,
        log_tf_ansible: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Show logs for the latest action for a workspace template.

        Show the Terraform logs for the most recent job of a template that ran against
        your workspace.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access to the workspace ID and the resource group. For more information, about
        Schematics access and permissions, see [Schematics service access roles and
        required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str t_id: The ID of the Terraform template or IBM Cloud catalog
               software template in the workspace.  Use the `GET /v1/workspaces` to look
               up the workspace IDs and template IDs or `template_data.id`.
        :param bool log_tf_cmd: (optional) Enter false to replace the first line in
               each Terraform command section, such as Terraform INIT or Terraform PLAN,
               with Schematics INIT (Schematics PLAN) in your log output.  In addition,
               the log lines Starting command: terraform init -input=false -no-color and
               Starting command: terraform apply -state=terraform.tfstate
               -var-file=schematics.tfvars -auto-approve -no-color are suppressed.  All
               subsequent command lines still use the Terraform command prefix. To remove
               this prefix, use the log_tf_prefix option.
        :param bool log_tf_prefix: (optional) `false` will hide all the terraform
               command prefix in the log statements.
        :param bool log_tf_null_resource: (optional) `false` will hide all the null
               resource prefix in the log statements.
        :param bool log_tf_ansible: (optional) `true` will format all logs to
               withhold the original format  of ansible output in the log statements.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `str` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_template_logs')
        headers.update(sdk_headers)

        params = {
            'log_tf_cmd': log_tf_cmd,
            'log_tf_prefix': log_tf_prefix,
            'log_tf_null_resource': log_tf_null_resource,
            'log_tf_ansible': log_tf_ansible
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id']
        path_param_values = self.encode_path_vars(w_id, t_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/runtime_data/{t_id}/log_store'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def get_template_activity_log(self,
        w_id: str,
        t_id: str,
        activity_id: str,
        *,
        log_tf_cmd: bool = None,
        log_tf_prefix: bool = None,
        log_tf_null_resource: bool = None,
        log_tf_ansible: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Show logs for a workspace job.

        Show the Terraform logs for an job that ran against your workspace.

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str t_id: The ID of the Terraform template or IBM Cloud catalog
               software template in the workspace.  Use the `GET /v1/workspaces` to look
               up the workspace IDs and template IDs or `template_data.id`.
        :param str activity_id: The ID of the activity or job, for which you want
               to retrieve details.  To find the job ID, use the `GET
               /v1/workspaces/{id}/actions` API.
        :param bool log_tf_cmd: (optional) Enter false to replace the first line in
               each Terraform command section, such as Terraform INIT or Terraform PLAN,
               with Schematics INIT (Schematics PLAN) in your log output.  In addition,
               the log lines Starting command: terraform init -input=false -no-color and
               Starting command: terraform apply -state=terraform.tfstate
               -var-file=schematics.tfvars -auto-approve -no-color are suppressed.  All
               subsequent command lines still use the Terraform command prefix. To remove
               this prefix, use the log_tf_prefix option.
        :param bool log_tf_prefix: (optional) `false` will hide all the terraform
               command prefix in the log statements.
        :param bool log_tf_null_resource: (optional) `false` will hide all the null
               resource prefix in the log statements.
        :param bool log_tf_ansible: (optional) `true` will format all logs to
               withhold the original format  of ansible output in the log statements.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `str` result
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if t_id is None:
            raise ValueError('t_id must be provided')
        if activity_id is None:
            raise ValueError('activity_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_template_activity_log')
        headers.update(sdk_headers)

        params = {
            'log_tf_cmd': log_tf_cmd,
            'log_tf_prefix': log_tf_prefix,
            'log_tf_null_resource': log_tf_null_resource,
            'log_tf_ansible': log_tf_ansible
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 't_id', 'activity_id']
        path_param_values = self.encode_path_vars(w_id, t_id, activity_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/runtime_data/{t_id}/log_store/actions/{activity_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response

    #########################
    # actions
    #########################


    def list_actions(self,
        *,
        offset: int = None,
        limit: int = None,
        sort: str = None,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List actions.

        Retrieve a list of all Schematics actions that depends on the API endpoint that
        you have access. For example, if you use an API endpoint for a geography, such as
        North America, only actions that are created in `us-south` or `us-east` are
        retrieved.
         For more information, about supported API endpoints, see
        [API endpoints](/apidocs/schematics#api-endpoints).
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to an action ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param int offset: (optional) The starting position of the item in the list
               of items. For example, if you have three workspaces in your account, the
               first workspace is assigned position number 0, the second workspace is
               assigned position number 1, and so forth. If you have 6 workspaces and you
               want to list the details for workspaces 2-6, enter 1. To limit the number
               of workspaces that is returned, use the `limit` option in addition to the
               `offset` option. Negative numbers are not supported and are ignored.
        :param int limit: (optional) The maximum number of items that you want to
               list. The number must be a positive integer between 1 and 2000. If no value
               is provided, 100 is used by default.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ActionList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_actions')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/actions'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def create_action(self,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        tags: List[str] = None,
        user_state: 'UserState' = None,
        source_readme_url: str = None,
        source: 'ExternalSource' = None,
        source_type: str = None,
        command_parameter: str = None,
        inventory: str = None,
        credentials: List['VariableData'] = None,
        bastion: 'BastionResourceDefinition' = None,
        bastion_credential: 'VariableData' = None,
        targets_ini: str = None,
        inputs: List['VariableData'] = None,
        outputs: List['VariableData'] = None,
        settings: List['VariableData'] = None,
        state: 'ActionState' = None,
        sys_lock: 'SystemLock' = None,
        x_github_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create an action.

        Create an IBM Cloud Schematics action to run on a single target or groups of
        target hosts, roles, policies, or steps to deploy your resources in the target
        hosts. You can run the IBM Cloud resources the order in which you want to execute
        them. **Note** If your Git repository already contains a host file. Schematics
        does not overwrite the host file already present in your Git repository. For
        sample templates, see IBM Cloud Automation
        [templates](https://github.com/Cloud-Schematics).
         For more information, about the Schematics create action,
         see [ibmcloud schematics action
        create](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-create-action).
         **Note** you cannot update the location and region once an action is created.
         Also, make sure your IP addresses are in the
        [allowlist](https://cloud.ibm.com/docs/schematics?topic=schematics-allowed-ipaddresses).
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to an action ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions.

        :param str name: (optional) The unique name of your action. The name can be
               up to 128 characters long and can include alphanumeric characters, spaces,
               dashes, and underscores. **Example** you can use the name to stop action.
        :param str description: (optional) Action description.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for an action.
               By default, action is created in default resource group.
        :param List[str] tags: (optional) Action tags.
        :param UserState user_state: (optional) User defined status of the
               Schematics object.
        :param str source_readme_url: (optional) URL of the `README` file, for the
               source URL.
        :param ExternalSource source: (optional) Source of templates, playbooks, or
               controls.
        :param str source_type: (optional) Type of source for the Template.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param str inventory: (optional) Target inventory record ID, used by the
               action or ansible playbook.
        :param List[VariableData] credentials: (optional) credentials of the
               Action.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param VariableData bastion_credential: (optional) User editable variable
               data & system generated reference to value.
        :param str targets_ini: (optional) Inventory of host and host group for the
               playbook in `INI` file format. For example, `"targets_ini":
               "[webserverhost]
                172.22.192.6
                [dbhost]
                172.22.192.5"`. For more information, about an inventory host group
               syntax, see [Inventory host
               groups](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-inventory-host-grps).
        :param List[VariableData] inputs: (optional) Input variables for the
               Action.
        :param List[VariableData] outputs: (optional) Output variables for the
               Action.
        :param List[VariableData] settings: (optional) Environment variables for
               the Action.
        :param ActionState state: (optional) Computed state of the Action.
        :param SystemLock sys_lock: (optional) System lock status.
        :param str x_github_token: (optional) The personal access token to
               authenticate with your private GitHub or GitLab repository and access your
               Terraform template.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Action` object
        """

        if user_state is not None:
            user_state = convert_model(user_state)
        if source is not None:
            source = convert_model(source)
        if credentials is not None:
            credentials = [convert_model(x) for x in credentials]
        if bastion is not None:
            bastion = convert_model(bastion)
        if bastion_credential is not None:
            bastion_credential = convert_model(bastion_credential)
        if inputs is not None:
            inputs = [convert_model(x) for x in inputs]
        if outputs is not None:
            outputs = [convert_model(x) for x in outputs]
        if settings is not None:
            settings = [convert_model(x) for x in settings]
        if state is not None:
            state = convert_model(state)
        if sys_lock is not None:
            sys_lock = convert_model(sys_lock)
        headers = {
            'X-Github-token': x_github_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_action')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'tags': tags,
            'user_state': user_state,
            'source_readme_url': source_readme_url,
            'source': source,
            'source_type': source_type,
            'command_parameter': command_parameter,
            'inventory': inventory,
            'credentials': credentials,
            'bastion': bastion,
            'bastion_credential': bastion_credential,
            'targets_ini': targets_ini,
            'inputs': inputs,
            'outputs': outputs,
            'settings': settings,
            'state': state,
            'sys_lock': sys_lock
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/actions'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def get_action(self,
        action_id: str,
        *,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get action details.

        Retrieve the detailed information of an actions from your IBM Cloud account.  This
        API returns a URL to the log file that you can retrieve by using  the `GET
        /v2/actions/{action_id}/logs` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to an action ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str action_id: Action Id.  Use GET /actions API to look up the
               Action Ids in your IBM Cloud account.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Action` object
        """

        if action_id is None:
            raise ValueError('action_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_action')
        headers.update(sdk_headers)

        params = {
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['action_id']
        path_param_values = self.encode_path_vars(action_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/actions/{action_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def delete_action(self,
        action_id: str,
        *,
        force: bool = None,
        propagate: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete an action.

        Delete a Schematics action and specify the Ansible playbook that you want to run
        against your IBM Cloud resources. **Note** you cannot delete or stop the job
        activity from an ongoing execution of an action defined in the playbook. You can
        repeat the execution of same job, whenever you patch the actions. For more
        information, about the Schematics action state, see  [Schematics action state
        diagram](https://cloud.ibm.com/docs/schematics?topic=schematics-action-setup#action-state-diagram).
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to an action ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions.

        :param str action_id: Action Id.  Use GET /actions API to look up the
               Action Ids in your IBM Cloud account.
        :param bool force: (optional) Equivalent to -force options in the command
               line.
        :param bool propagate: (optional) Auto propagate the chaange or deletion to
               the dependent resources.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if action_id is None:
            raise ValueError('action_id must be provided')
        headers = {
            'force': force,
            'propagate': propagate
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_action')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        path_param_keys = ['action_id']
        path_param_values = self.encode_path_vars(action_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/actions/{action_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def update_action(self,
        action_id: str,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        tags: List[str] = None,
        user_state: 'UserState' = None,
        source_readme_url: str = None,
        source: 'ExternalSource' = None,
        source_type: str = None,
        command_parameter: str = None,
        inventory: str = None,
        credentials: List['VariableData'] = None,
        bastion: 'BastionResourceDefinition' = None,
        bastion_credential: 'VariableData' = None,
        targets_ini: str = None,
        inputs: List['VariableData'] = None,
        outputs: List['VariableData'] = None,
        settings: List['VariableData'] = None,
        state: 'ActionState' = None,
        sys_lock: 'SystemLock' = None,
        x_github_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update an action.

        Update or replace an action to change the action state from the critical state to
        normal state, or pending state to the normal state for a successful execution.
        For more information, about the Schematics action state, see [Schematics action
        state
        diagram](https://cloud.ibm.com/docs/schematics?topic=schematics-action-setup#action-state-diagram).
         **Note** you cannot update the location and region once an action is created.
         Also, make sure your IP addresses are in the
        [allowlist](https://cloud.ibm.com/docs/schematics?topic=schematics-allowed-ipaddresses].
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to an action ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions.

        :param str action_id: Action Id.  Use GET /actions API to look up the
               Action Ids in your IBM Cloud account.
        :param str name: (optional) The unique name of your action. The name can be
               up to 128 characters long and can include alphanumeric characters, spaces,
               dashes, and underscores. **Example** you can use the name to stop action.
        :param str description: (optional) Action description.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for an action.
               By default, action is created in default resource group.
        :param List[str] tags: (optional) Action tags.
        :param UserState user_state: (optional) User defined status of the
               Schematics object.
        :param str source_readme_url: (optional) URL of the `README` file, for the
               source URL.
        :param ExternalSource source: (optional) Source of templates, playbooks, or
               controls.
        :param str source_type: (optional) Type of source for the Template.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param str inventory: (optional) Target inventory record ID, used by the
               action or ansible playbook.
        :param List[VariableData] credentials: (optional) credentials of the
               Action.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param VariableData bastion_credential: (optional) User editable variable
               data & system generated reference to value.
        :param str targets_ini: (optional) Inventory of host and host group for the
               playbook in `INI` file format. For example, `"targets_ini":
               "[webserverhost]
                172.22.192.6
                [dbhost]
                172.22.192.5"`. For more information, about an inventory host group
               syntax, see [Inventory host
               groups](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-inventory-host-grps).
        :param List[VariableData] inputs: (optional) Input variables for the
               Action.
        :param List[VariableData] outputs: (optional) Output variables for the
               Action.
        :param List[VariableData] settings: (optional) Environment variables for
               the Action.
        :param ActionState state: (optional) Computed state of the Action.
        :param SystemLock sys_lock: (optional) System lock status.
        :param str x_github_token: (optional) The personal access token to
               authenticate with your private GitHub or GitLab repository and access your
               Terraform template.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Action` object
        """

        if action_id is None:
            raise ValueError('action_id must be provided')
        if user_state is not None:
            user_state = convert_model(user_state)
        if source is not None:
            source = convert_model(source)
        if credentials is not None:
            credentials = [convert_model(x) for x in credentials]
        if bastion is not None:
            bastion = convert_model(bastion)
        if bastion_credential is not None:
            bastion_credential = convert_model(bastion_credential)
        if inputs is not None:
            inputs = [convert_model(x) for x in inputs]
        if outputs is not None:
            outputs = [convert_model(x) for x in outputs]
        if settings is not None:
            settings = [convert_model(x) for x in settings]
        if state is not None:
            state = convert_model(state)
        if sys_lock is not None:
            sys_lock = convert_model(sys_lock)
        headers = {
            'X-Github-token': x_github_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_action')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'tags': tags,
            'user_state': user_state,
            'source_readme_url': source_readme_url,
            'source': source,
            'source_type': source_type,
            'command_parameter': command_parameter,
            'inventory': inventory,
            'credentials': credentials,
            'bastion': bastion,
            'bastion_credential': bastion_credential,
            'targets_ini': targets_ini,
            'inputs': inputs,
            'outputs': outputs,
            'settings': settings,
            'state': state,
            'sys_lock': sys_lock
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['action_id']
        path_param_values = self.encode_path_vars(action_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/actions/{action_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PATCH',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def upload_template_tar_action(self,
        action_id: str,
        *,
        file: BinaryIO = None,
        file_content_type: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Upload a TAR file to an action.

        Update your template by uploading tape archive file (.tar) file from  your local
        machine. Before you use this API, you must create an action  without a link to a
        GitHub or GitLab repository with the `POST /v2/actions` API.
        <h3>Authorization</h3>
          Schematics support generic authorization such as service access or  platform
        access to an action ID and the resource group.  For more information, about
        Schematics access and permissions, see  [Schematics service access roles and
        required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions.

        :param str action_id: Action Id.  Use GET /actions API to look up the
               Action Ids in your IBM Cloud account.
        :param BinaryIO file: (optional) Template tar file.
        :param str file_content_type: (optional) The content type of file.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `TemplateRepoTarUploadResponse` object
        """

        if action_id is None:
            raise ValueError('action_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='upload_template_tar_action')
        headers.update(sdk_headers)

        form_data = []
        if file:
            form_data.append(('file', (None, file, file_content_type or 'application/octet-stream')))

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['action_id']
        path_param_values = self.encode_path_vars(action_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/actions/{action_id}/template_repo_upload'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       files=form_data)

        response = self.send(request, **kwargs)
        return response

    #########################
    # jobs
    #########################


    def list_workspace_activities(self,
        w_id: str,
        *,
        offset: int = None,
        limit: int = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List all workspace jobs.

        Retrieve a list of all jobs that ran against a workspace. Jobs are generated when
        you use the `apply`, `plan`, `destroy`, and `refresh`,   command API.

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param int offset: (optional) The starting position of the item in the list
               of items. For example, if you have three workspaces in your account, the
               first workspace is assigned position number 0, the second workspace is
               assigned position number 1, and so forth. If you have 6 workspaces and you
               want to list the details for workspaces 2-6, enter 1. To limit the number
               of workspaces that is returned, use the `limit` option in addition to the
               `offset` option. Negative numbers are not supported and are ignored.
        :param int limit: (optional) The maximum number of items that you want to
               list. The number must be a positive integer between 1 and 2000. If no value
               is provided, 100 is used by default.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivities` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_workspace_activities')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/actions'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_activity(self,
        w_id: str,
        activity_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get workspace job details.

        Get the details for a workspace job that ran against the workspace. This API
        returns the job status and a URL to the log file that you can  retrieve by using
        the `GET /v1/workspaces/{id}/actions/{action_id}/logs` API.

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str activity_id: The ID of the activity or job, for which you want
               to retrieve details.  To find the job ID, use the `GET
               /v1/workspaces/{id}/actions` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivity` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if activity_id is None:
            raise ValueError('activity_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_activity')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 'activity_id']
        path_param_values = self.encode_path_vars(w_id, activity_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/actions/{activity_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def delete_workspace_activity(self,
        w_id: str,
        activity_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Stop the workspace job.

        Stop an ongoing schematics job that runs against your workspace.
        **Note**: If you remove the Schematics apply job that runs against your workspace,
         any changes to your IBM Cloud resources that are already applied are not
        reverted.  If a creation, update, or deletion is currently in progress, Schematics
        waits for  the job to be completed first. Then, any other resource creations,
        updates, or  deletions that are included in your Terraform template file are
        ignored.
        <h3>Authorization</h3>  Schematics supports generic authorization such as service
        access or platform access  to the workspace ID and the resource group. For more
        information, about Schematics  access and permissions, see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str activity_id: The ID of the activity or job, for which you want
               to retrieve details.  To find the job ID, use the `GET
               /v1/workspaces/{id}/actions` API.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityApplyResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if activity_id is None:
            raise ValueError('activity_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_workspace_activity')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id', 'activity_id']
        path_param_values = self.encode_path_vars(w_id, activity_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/actions/{activity_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def run_workspace_commands(self,
        w_id: str,
        refresh_token: str,
        *,
        commands: List['TerraformCommand'] = None,
        operation_name: str = None,
        description: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Run Terraform Commands.

        Run Terraform state commands to modify the workspace state file, by using the IBM
        Cloud Schematics API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access
         to the workspace ID and the resource group. For more information, about
        Schematics
         access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace.  To find the workspace ID, use
               the `GET /v1/workspaces` API.
        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param List[TerraformCommand] commands: (optional) List of commands.  You
               can execute single set of commands or multiple commands.  For more
               information, about the payload of the multiple commands,  refer to
               [Commands](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#commands).
        :param str operation_name: (optional) Command name.
        :param str description: (optional) Command description.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityCommandResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if commands is not None:
            commands = [convert_model(x) for x in commands]
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='run_workspace_commands')
        headers.update(sdk_headers)

        data = {
            'commands': commands,
            'operation_name': operation_name,
            'description': description
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/commands'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def apply_workspace_command(self,
        w_id: str,
        refresh_token: str,
        *,
        action_options: 'WorkspaceActivityOptionsTemplate' = None,
        delegated_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Perform a Schematics `apply` job.

        Run a Schematics `apply` job against your workspace. An `apply` job provisions,
        modifies, or removes the IBM Cloud resources that you described in the Terraform
        template that your workspace points to. Depending on the type and number of
        resources that you want to provision or modify, this process might take a few
        minutes, or even up to hours to complete. During this time, you cannot make
        changes to your workspace. After all updates are applied, the state of the files
        is
        [persisted](https://cloud.ibm.com/docs/schematics?topic=schematics-persist-files)
        to determine what resources exist in your IBM Cloud account.
         **Important**: Your workspace must be in an `Inactive`, `Active`, `Failed`, or
         `Stopped` state to perform a Schematics `apply` job. After all updates are
        applied,
         the state of the files is
        [persisted](https://cloud.ibm.com/docs/schematics?topic=schematics-persist-files)
         to determine what resources exist in your IBM Cloud account.
         **Note**: This API returns an activity or job ID that you use to retrieve the
         log URL with the `GET /v1/workspaces/{id}/actions/{action_id}/logs` API.
         **Important:** Applying a template might incur costs. Make sure to review
         the pricing information for the resources that you specified in your
         templates before you apply the template in IBM Cloud.
         To find a summary of job that Schematics is about to perform,
         create a Terraform execution plan with the `POST /v1/workspaces/{id}/plan` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace for which you want to run a
               Schematics `apply` job.  To find the workspace ID, use the `GET
               /workspaces` API.
        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param WorkspaceActivityOptionsTemplate action_options: (optional)
               Workspace job options template.
        :param str delegated_token: (optional) The IAM delegated token for your IBM
               Cloud account.  This token is required for requests that are sent via the
               UI only.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityApplyResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if action_options is not None:
            action_options = convert_model(action_options)
        headers = {
            'refresh_token': refresh_token,
            'delegated_token': delegated_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='apply_workspace_command')
        headers.update(sdk_headers)

        data = {
            'action_options': action_options
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/apply'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def destroy_workspace_command(self,
        w_id: str,
        refresh_token: str,
        *,
        action_options: 'WorkspaceActivityOptionsTemplate' = None,
        delegated_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Perform a Schematics `destroy` job.

        Run a Schematics `destroy` job against your workspace. A `destroy` job removes all
        IBM Cloud resources that are associated with your workspace. Removing your
        resources does not delete the Schematics workspace. To delete the workspace, use
        the `DELETE /v1/workspaces/{id}` API. This API returns an activity or job ID that
        you use to retrieve the URL to the log file with the `GET
        /v1/workspaces/{id}/actions/{action_id}/logs` API.
         **Important**: Your workspace must be in an `Active`, `Failed`, or `Stopped`
        state to perform a Schematics `destroy` job.
         **Note**: Deleting IBM Cloud resources cannot be undone. Make sure that you back
        up any required data before you remove your resources.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access
          to the workspace ID and the resource group.
          For more information, about Schematics access and permissions,
          see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace for which you want to perform a
               Schematics `destroy` job.  To find the workspace ID, use the `GET
               /workspaces` API.
        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param WorkspaceActivityOptionsTemplate action_options: (optional)
               Workspace job options template.
        :param str delegated_token: (optional) The IAM delegated token for your IBM
               Cloud account.  This token is required for requests that are sent via the
               UI only.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityDestroyResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if action_options is not None:
            action_options = convert_model(action_options)
        headers = {
            'refresh_token': refresh_token,
            'delegated_token': delegated_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='destroy_workspace_command')
        headers.update(sdk_headers)

        data = {
            'action_options': action_options
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/destroy'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def plan_workspace_command(self,
        w_id: str,
        refresh_token: str,
        *,
        delegated_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Perform a Schematics `plan` job.

        Run a Schematics `plan` job against your workspace. The `plan` job creates a
        summary of IBM Cloud resources that must be created, modified, or deleted to
        achieve the state that is described in the Terraform or IBM Cloud catalog template
        that your workspace points to. During this time, you cannot make changes to your
        workspace. You can use the summary to verify your changes before you apply the
        template in IBM Cloud.
         **Important**: Your workspace must be in an `Inactive`, `Active`, `Failed`, or
        `Stopped` state to perform a Schematics `plan` job.
         **Note**: This API returns an activity or job ID that you use to retrieve the URL
        to the log file with the `GET /v1/workspaces/{id}/actions/{action_id}/logs` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access
         to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace, for which you want to run a
               Schematics `plan` job.  To find the ID of your workspace, use the `GET
               /v1/workspaces` API.
        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param str delegated_token: (optional) The IAM delegated token for your IBM
               Cloud account.  This token is required for requests that are sent via the
               UI only.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityPlanResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token,
            'delegated_token': delegated_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='plan_workspace_command')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/plan'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def refresh_workspace_command(self,
        w_id: str,
        refresh_token: str,
        *,
        delegated_token: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Perform a Schematics `refresh` job.

        Run a Schematics `refresh` job against your workspace. A `refresh` job validates
        the IBM Cloud resources in your account against the state that is stored in the
        Terraform statefile of your workspace. If differences are found, the Terraform
        statefile is updated accordingly. This API returns an activity or job ID that you
        use to retrieve the URL to the log file with the `GET
        /v1/workspaces/{id}/actions/{action_id}/logs` API.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access
         to the workspace ID and the resource group.
         For more information, about Schematics access and permissions,
         see [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str w_id: The ID of the workspace, for which you want to run a
               Schematics `refresh` job.  To find the ID of your workspace, use the `GET
               /v1/workspaces` API.
        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param str delegated_token: (optional) The IAM delegated token for your IBM
               Cloud account.  This token is required for requests that are sent via the
               UI only.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceActivityRefreshResult` object
        """

        if w_id is None:
            raise ValueError('w_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token,
            'delegated_token': delegated_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='refresh_workspace_command')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['w_id']
        path_param_values = self.encode_path_vars(w_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspaces/{w_id}/refresh'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def list_jobs(self,
        *,
        offset: int = None,
        limit: int = None,
        sort: str = None,
        profile: str = None,
        resource: str = None,
        resource_id: str = None,
        action_id: str = None,
        list: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List jobs.

        Retrieve a list of all Schematics jobs.  The job displays a list of jobs with the
        status as `pending`, `in_progess`,  `success`, or `failed`. Jobs are generated
        when you use the  `POST /v2/jobs`, `PUT /v2/jobs/{job_id}`, or `DELETE
        /v2/jobs/{job_id}`.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to the job ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param int offset: (optional) The starting position of the item in the list
               of items. For example, if you have three workspaces in your account, the
               first workspace is assigned position number 0, the second workspace is
               assigned position number 1, and so forth. If you have 6 workspaces and you
               want to list the details for workspaces 2-6, enter 1. To limit the number
               of workspaces that is returned, use the `limit` option in addition to the
               `offset` option. Negative numbers are not supported and are ignored.
        :param int limit: (optional) The maximum number of items that you want to
               list. The number must be a positive integer between 1 and 2000. If no value
               is provided, 100 is used by default.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param str profile: (optional) Level of details returned by the get method.
        :param str resource: (optional) Name of the resource (workspace, actions or
               controls).
        :param str resource_id: (optional) The Resource Id. It could be an
               Action-id or Workspace-id.
        :param str action_id: (optional) Action Id.
        :param str list: (optional) list jobs.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `JobList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_jobs')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'profile': profile,
            'resource': resource,
            'resource_id': resource_id,
            'action_id': action_id,
            'list': list
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/jobs'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def create_job(self,
        refresh_token: str,
        *,
        command_object: str = None,
        command_object_id: str = None,
        command_name: str = None,
        command_parameter: str = None,
        command_options: List[str] = None,
        inputs: List['VariableData'] = None,
        settings: List['VariableData'] = None,
        tags: List[str] = None,
        location: str = None,
        status: 'JobStatus' = None,
        data: 'JobData' = None,
        bastion: 'BastionResourceDefinition' = None,
        log_summary: 'JobLogSummary' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a job.

        Create & launch the Schematics job. It can be used to launch an Ansible playbook
        against a target hosts.  The job displays a list of jobs with the status as
        `pending`, `in_progess`, `success`, or `failed`.

        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_id: (optional) Job command object id
               (workspace-id, action-id).
        :param str command_name: (optional) Schematics job command name.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param List[str] command_options: (optional) Command line options for the
               command.
        :param List[VariableData] inputs: (optional) Job inputs used by Action or
               Workspace.
        :param List[VariableData] settings: (optional) Environment variables used
               by the Job while performing Action or Workspace.
        :param List[str] tags: (optional) User defined tags, while running the job.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param JobStatus status: (optional) Job Status.
        :param JobData data: (optional) Job data.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Job` object
        """

        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if inputs is not None:
            inputs = [convert_model(x) for x in inputs]
        if settings is not None:
            settings = [convert_model(x) for x in settings]
        if status is not None:
            status = convert_model(status)
        if data is not None:
            data = convert_model(data)
        if bastion is not None:
            bastion = convert_model(bastion)
        if log_summary is not None:
            log_summary = convert_model(log_summary)
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_job')
        headers.update(sdk_headers)

        data = {
            'command_object': command_object,
            'command_object_id': command_object_id,
            'command_name': command_name,
            'command_parameter': command_parameter,
            'command_options': command_options,
            'inputs': inputs,
            'settings': settings,
            'tags': tags,
            'location': location,
            'status': status,
            'data': data,
            'bastion': bastion,
            'log_summary': log_summary
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/jobs'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def get_job(self,
        job_id: str,
        *,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get a job.

        Retrieve the detailed information of Job
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to the job ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str job_id: Job Id. Use `GET /v2/jobs` API to look up the Job Ids in
               your IBM Cloud account.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Job` object
        """

        if job_id is None:
            raise ValueError('job_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_job')
        headers.update(sdk_headers)

        params = {
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['job_id']
        path_param_values = self.encode_path_vars(job_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/jobs/{job_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def update_job(self,
        job_id: str,
        refresh_token: str,
        *,
        command_object: str = None,
        command_object_id: str = None,
        command_name: str = None,
        command_parameter: str = None,
        command_options: List[str] = None,
        inputs: List['VariableData'] = None,
        settings: List['VariableData'] = None,
        tags: List[str] = None,
        location: str = None,
        status: 'JobStatus' = None,
        data: 'JobData' = None,
        bastion: 'BastionResourceDefinition' = None,
        log_summary: 'JobLogSummary' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update a job.

        Creates a copy of the Schematics job and relaunches an existing job  by updating
        the information of an existing Schematics job.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to the job ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str job_id: Job Id. Use `GET /v2/jobs` API to look up the Job Ids in
               your IBM Cloud account.
        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_id: (optional) Job command object id
               (workspace-id, action-id).
        :param str command_name: (optional) Schematics job command name.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param List[str] command_options: (optional) Command line options for the
               command.
        :param List[VariableData] inputs: (optional) Job inputs used by Action or
               Workspace.
        :param List[VariableData] settings: (optional) Environment variables used
               by the Job while performing Action or Workspace.
        :param List[str] tags: (optional) User defined tags, while running the job.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param JobStatus status: (optional) Job Status.
        :param JobData data: (optional) Job data.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Job` object
        """

        if job_id is None:
            raise ValueError('job_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        if inputs is not None:
            inputs = [convert_model(x) for x in inputs]
        if settings is not None:
            settings = [convert_model(x) for x in settings]
        if status is not None:
            status = convert_model(status)
        if data is not None:
            data = convert_model(data)
        if bastion is not None:
            bastion = convert_model(bastion)
        if log_summary is not None:
            log_summary = convert_model(log_summary)
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_job')
        headers.update(sdk_headers)

        data = {
            'command_object': command_object,
            'command_object_id': command_object_id,
            'command_name': command_name,
            'command_parameter': command_parameter,
            'command_options': command_options,
            'inputs': inputs,
            'settings': settings,
            'tags': tags,
            'location': location,
            'status': status,
            'data': data,
            'bastion': bastion,
            'log_summary': log_summary
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['job_id']
        path_param_values = self.encode_path_vars(job_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/jobs/{job_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def delete_job(self,
        job_id: str,
        refresh_token: str,
        *,
        force: bool = None,
        propagate: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Stop the running Job, and delete the Job.

        Stop the running Job, and delete the Job.  **Note** You cannot delete or stop the
        job activity from an ongoing  execution of an action defined in the playbook.  You
        can repeat the execution of same job, whenever you patch or update the action or
        workspace.
         <h3>Authorization</h3>
         Schematics support generic authorization such as service access or
         platform access to the job ID and the resource group.
         For more information, about Schematics access and permissions, see
         [Schematics service access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str job_id: Job Id. Use `GET /v2/jobs` API to look up the Job Ids in
               your IBM Cloud account.
        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param bool force: (optional) Equivalent to -force options in the command
               line.
        :param bool propagate: (optional) Auto propagate the chaange or deletion to
               the dependent resources.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if job_id is None:
            raise ValueError('job_id must be provided')
        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token,
            'force': force,
            'propagate': propagate
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_job')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        path_param_keys = ['job_id']
        path_param_values = self.encode_path_vars(job_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/jobs/{job_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def list_job_logs(self,
        job_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get job logs.

        Retrieve the job logs
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or  platform access to the action ID and the resource group.  For more
        information, about Schematics access and permissions, see  [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str job_id: Job Id. Use `GET /v2/jobs` API to look up the Job Ids in
               your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `JobLog` object
        """

        if job_id is None:
            raise ValueError('job_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_job_logs')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['job_id']
        path_param_values = self.encode_path_vars(job_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/jobs/{job_id}/logs'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response

    #########################
    # bulk-jobs
    #########################


    def create_workspace_deletion_job(self,
        refresh_token: str,
        *,
        new_delete_workspaces: bool = None,
        new_destroy_resources: bool = None,
        new_job: str = None,
        new_version: str = None,
        new_workspaces: List[str] = None,
        destroy_resources: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete multiple workspaces.

        Delete multiple workspaces.  Use ?destroy_resource="true" to destroy the related
        cloud resources,  otherwise the resources must be managed outside of Schematics.

        :param str refresh_token: The IAM refresh token for the user or service
               identity.
                 **Retrieving refresh token**:
                 * Use `export IBMCLOUD_API_KEY=<ibmcloud_api_key>`, and execute `curl -X
               POST "https://iam.cloud.ibm.com/identity/token" -H "Content-Type:
               application/x-www-form-urlencoded" -d
               "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$IBMCLOUD_API_KEY"
               -u bx:bx`.
                 * For more information, about creating IAM access token and API Docs,
               refer, [IAM access
               token](/apidocs/iam-identity-token-api#gettoken-password) and [Create API
               key](/apidocs/iam-identity-token-api#create-api-key).
                 **Limitation**:
                 * If the token is expired, you can use `refresh token` to get a new IAM
               access token.
                 * The `refresh_token` parameter cannot be used to retrieve a new IAM
               access token.
                 * When the IAM access token is about to expire, use the API key to create
               a new access token.
        :param bool new_delete_workspaces: (optional) True to delete workspace.
        :param bool new_destroy_resources: (optional) True to destroy the resources
               managed by this workspace.
        :param str new_job: (optional) Workspace deletion job name.
        :param str new_version: (optional) Version of the terraform template.
        :param List[str] new_workspaces: (optional) List of workspaces to be
               deleted.
        :param str destroy_resources: (optional) If set to `true`, refresh_token
               header configuration is required to delete all the Terraform resources, and
               the Schematics workspace. If set to `false`, you can remove only the
               workspace. Your Terraform resources are still available and must be managed
               with the resource dashboard or CLI.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceBulkDeleteResponse` object
        """

        if refresh_token is None:
            raise ValueError('refresh_token must be provided')
        headers = {
            'refresh_token': refresh_token
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_workspace_deletion_job')
        headers.update(sdk_headers)

        params = {
            'destroy_resources': destroy_resources
        }

        data = {
            'delete_workspaces': new_delete_workspaces,
            'destroy_resources': new_destroy_resources,
            'job': new_job,
            'version': new_version,
            'workspaces': new_workspaces
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v1/workspace_jobs'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def get_workspace_deletion_job_status(self,
        wj_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the workspace deletion job status.

        Get the workspace deletion job status.

        :param str wj_id: The workspace job ID.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `WorkspaceJobResponse` object
        """

        if wj_id is None:
            raise ValueError('wj_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_workspace_deletion_job_status')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['wj_id']
        path_param_values = self.encode_path_vars(wj_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v1/workspace_jobs/{wj_id}/status'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response

    #########################
    # inventory
    #########################


    def list_inventories(self,
        *,
        offset: int = None,
        limit: int = None,
        sort: str = None,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List all inventory definitions.

        Retrieve a list of all Schematics inventories that depends on the API endpoint
        that you have access. For example, if you use an API endpoint for a geography,
        such as North America, only inventories that are created in `us-south` or
        `us-east` are retrieved. For more information, about supported API endpoints, see
        [APIendpoints](/apidocs/schematics#api-endpoints).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions, see  [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param int offset: (optional) The starting position of the item in the list
               of items. For example, if you have three workspaces in your account, the
               first workspace is assigned position number 0, the second workspace is
               assigned position number 1, and so forth. If you have 6 workspaces and you
               want to list the details for workspaces 2-6, enter 1. To limit the number
               of workspaces that is returned, use the `limit` option in addition to the
               `offset` option. Negative numbers are not supported and are ignored.
        :param int limit: (optional) The maximum number of items that you want to
               list. The number must be a positive integer between 1 and 2000. If no value
               is provided, 100 is used by default.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecordList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_inventories')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/inventories'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def create_inventory(self,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        inventories_ini: str = None,
        resource_queries: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create an inventory definition.

        Create an IBM Cloud Schematics inventory as a single IBM Cloud resource where you
        want to run Ansible playbook by using Schematics actions. For more information,
        about inventory host groups, refer to [creating static and dynamic inventory for
        Schematics
        actions](https://cloud.ibm.com/docs/schematics?topic=schematics-inventories-setup).
        **Note** you cannot update the location and region, resource group once an action
        is created.  Also, make sure your IP addresses are in the
        [allowlist](https://cloud.ibm.com/docs/schematics?topic=schematics-allowed-ipaddresses).
         If your Git repository already contains a host file. Schematics does not
        overwrite the host file already present in your Git repository.
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions, see  [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str name: (optional) The unique name of your Inventory definition.
               The name can be up to 128 characters long and can include alphanumeric
               characters, spaces, dashes, and underscores.
        :param str description: (optional) The description of your Inventory
               definition. The description can be up to 2048 characters long in size.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Inventory
               definition.   By default, Inventory definition will be created in Default
               Resource Group.
        :param str inventories_ini: (optional) Input inventory of host and host
               group for the playbook, in the `.ini` file format.
        :param List[str] resource_queries: (optional) Input resource query
               definitions that is used to dynamically generate the inventory of host and
               host group for the playbook.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_inventory')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'inventories_ini': inventories_ini,
            'resource_queries': resource_queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/inventories'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def get_inventory(self,
        inventory_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the inventory definition.

        Use this API to retrieve the detailed information for a resource inventory
        definition used to target an action in your IBM Cloud account. For more
        information, about inventory get, refer to [ibmcloud schematics inventory
        get](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-get-inv).
         **Note** you can fetch only the location and region, resource group from where
        your inventory is created.
         Also, make sure your IP addresses are in the
        [allowlist](https://cloud.ibm.com/docs/schematics?topic=schematics-allowed-ipaddresses).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions, see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str inventory_id: Resource Inventory Id.  Use `GET /v2/inventories`
               API to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_inventory')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def replace_inventory(self,
        inventory_id: str,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        inventories_ini: str = None,
        resource_queries: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace an inventory definition.

        Use this API to update the inventory definition resource used to target an action.
        For more information, about inventory update, refer to [ibmcloud schematics
        inventory
        update](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-update-inv).
         **Note** you cannot update the location and region, resource group once an action
        is created.
         Also, make sure your IP addresses are in the
        [allowlist](https://cloud.ibm.com/docs/schematics?topic=schematics-allowed-ipaddresses).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions, see  [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str inventory_id: Resource Inventory Id.  Use `GET /v2/inventories`
               API to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param str name: (optional) The unique name of your Inventory definition.
               The name can be up to 128 characters long and can include alphanumeric
               characters, spaces, dashes, and underscores.
        :param str description: (optional) The description of your Inventory
               definition. The description can be up to 2048 characters long in size.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Inventory
               definition.   By default, Inventory definition will be created in Default
               Resource Group.
        :param str inventories_ini: (optional) Input inventory of host and host
               group for the playbook, in the `.ini` file format.
        :param List[str] resource_queries: (optional) Input resource query
               definitions that is used to dynamically generate the inventory of host and
               host group for the playbook.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_inventory')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'inventories_ini': inventories_ini,
            'resource_queries': resource_queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def delete_inventory(self,
        inventory_id: str,
        *,
        force: bool = None,
        propagate: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete inventory definition.

        Use this API to delete the resource inventory definition by using the inventory ID
        that you want to run against. For more information, about inventory delete, refer
        to [ibmcloud schematics inventory
        delete](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-delete-inventory).
         **Note** you cannot delete the location and region, resource group from where
        your inventory is created.
         Also, make sure your IP addresses are in the
        [allowlist](https://cloud.ibm.com/docs/schematics?topic=schematics-allowed-ipaddresses).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions, see  [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str inventory_id: Resource Inventory Id.  Use `GET /v2/inventories`
               API to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param bool force: (optional) Equivalent to -force options in the command
               line.
        :param bool propagate: (optional) Auto propagate the chaange or deletion to
               the dependent resources.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {
            'force': force,
            'propagate': propagate
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_inventory')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def update_inventory(self,
        inventory_id: str,
        *,
        name: str = None,
        description: str = None,
        location: str = None,
        resource_group: str = None,
        inventories_ini: str = None,
        resource_queries: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update the inventory definition.

        Update the resource inventory definition.

        :param str inventory_id: Resource Inventory Id.  Use `GET /v2/inventories`
               API to look up the Resource Inventory definition Ids  in your IBM Cloud
               account.
        :param str name: (optional) The unique name of your Inventory definition.
               The name can be up to 128 characters long and can include alphanumeric
               characters, spaces, dashes, and underscores.
        :param str description: (optional) The description of your Inventory
               definition. The description can be up to 2048 characters long in size.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Inventory
               definition.   By default, Inventory definition will be created in Default
               Resource Group.
        :param str inventories_ini: (optional) Input inventory of host and host
               group for the playbook, in the `.ini` file format.
        :param List[str] resource_queries: (optional) Input resource query
               definitions that is used to dynamically generate the inventory of host and
               host group for the playbook.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `InventoryResourceRecord` object
        """

        if inventory_id is None:
            raise ValueError('inventory_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_inventory')
        headers.update(sdk_headers)

        data = {
            'name': name,
            'description': description,
            'location': location,
            'resource_group': resource_group,
            'inventories_ini': inventories_ini,
            'resource_queries': resource_queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['inventory_id']
        path_param_values = self.encode_path_vars(inventory_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/inventories/{inventory_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PATCH',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response

    #########################
    # resource-query
    #########################


    def list_resource_query(self,
        *,
        offset: int = None,
        limit: int = None,
        sort: str = None,
        profile: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List resource queries.

        Retrieve the list of resource query definitions that you have access to.  The list
        of resource queries that is returned depends on the API  endpoint that you use.
        For example, if you use an API endpoint for a geography, such as North America,
        only resource query definitions that are created in `us-south` or `us-east` are
        retrieved. For more information, about supported API endpoints, see [API
        endpoints](/apidocs/schematics#api-endpoints).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions,  see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param int offset: (optional) The starting position of the item in the list
               of items. For example, if you have three workspaces in your account, the
               first workspace is assigned position number 0, the second workspace is
               assigned position number 1, and so forth. If you have 6 workspaces and you
               want to list the details for workspaces 2-6, enter 1. To limit the number
               of workspaces that is returned, use the `limit` option in addition to the
               `offset` option. Negative numbers are not supported and are ignored.
        :param int limit: (optional) The maximum number of items that you want to
               list. The number must be a positive integer between 1 and 2000. If no value
               is provided, 100 is used by default.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param str profile: (optional) Level of details returned by the get method.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryRecordList` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_resource_query')
        headers.update(sdk_headers)

        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort,
            'profile': profile
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/resources_query'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def create_resource_query(self,
        *,
        type: str = None,
        name: str = None,
        queries: List['ResourceQuery'] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create resource query.

        Use this API to create a resource query definition that will be used to select an
        IBM Cloud resource or a group of resources as the dynamic inventory for the
        Schematics Actions.  For more information, about resource query commands, refer to
         [ibmcloud schematics resource query
        create](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-create-rq).
         **Note** you cannot update the location and region, resource group  once an
        action is created. Also, make sure your IP addresses are  in the
        [allowlist](https://cloud.ibm.com/docs/schematics?topic=schematics-allowed-ipaddresses).
         If your Git repository already contains a host file.  Schematics does not
        overwrite the host file already present in your Git repository.
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions,  see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str type: (optional) Resource type (cluster, vsi, icd, vpc).
        :param str name: (optional) Resource query name.
        :param List[ResourceQuery] queries: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryRecord` object
        """

        if queries is not None:
            queries = [convert_model(x) for x in queries]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_resource_query')
        headers.update(sdk_headers)

        data = {
            'type': type,
            'name': name,
            'queries': queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/resources_query'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def get_resources_query(self,
        query_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get resources query.

        Use this API to retrieve the information resource query by Id.  For more
        information, about resource query commands, refer to  [ibmcloud schematics
        resource query
        get](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-get-rq).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions,  see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str query_id: Resource query Id.  Use `GET /v2/resource_query` API
               to look up the Resource query definition Ids  in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryRecord` object
        """

        if query_id is None:
            raise ValueError('query_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_resources_query')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['query_id']
        path_param_values = self.encode_path_vars(query_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/resources_query/{query_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def replace_resources_query(self,
        query_id: str,
        *,
        type: str = None,
        name: str = None,
        queries: List['ResourceQuery'] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace resources query definition.

        Use this API to replace the resource query definition used to build  the dynamic
        inventory for the Schematics Action.  For more information, about resource query
        commands, refer to [ibmcloud schematics resource query
        update](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-update-rq).
        **Note** you cannot update the location and region, resource group  once a
        resource query is created. Also, make sure your IP addresses  are in the
        [allowlist](https://cloud.ibm.com/docs/schematics?topic=schematics-allowed-ipaddresses).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions,  see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str query_id: Resource query Id.  Use `GET /v2/resource_query` API
               to look up the Resource query definition Ids  in your IBM Cloud account.
        :param str type: (optional) Resource type (cluster, vsi, icd, vpc).
        :param str name: (optional) Resource query name.
        :param List[ResourceQuery] queries: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryRecord` object
        """

        if query_id is None:
            raise ValueError('query_id must be provided')
        if queries is not None:
            queries = [convert_model(x) for x in queries]
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='replace_resources_query')
        headers.update(sdk_headers)

        data = {
            'type': type,
            'name': name,
            'queries': queries
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['query_id']
        path_param_values = self.encode_path_vars(query_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/resources_query/{query_id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def execute_resource_query(self,
        query_id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Run the resource query.

        Run the resource query.

        :param str query_id: Resource query Id.  Use `GET /v2/resource_query` API
               to look up the Resource query definition Ids  in your IBM Cloud account.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ResourceQueryResponseRecord` object
        """

        if query_id is None:
            raise ValueError('query_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='execute_resource_query')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['query_id']
        path_param_values = self.encode_path_vars(query_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/resources_query/{query_id}'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response


    def delete_resources_query(self,
        query_id: str,
        *,
        force: bool = None,
        propagate: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete resources query.

        Use this API to delete the resource query definition by Id.  For more information,
        about resource query commands, refer to  [ibmcloud schematics resource query
        delete](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-delete-resource-query).
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to an action ID and the resource group. For more
        information, about Schematics access and permissions,  see [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#action-permissions).

        :param str query_id: Resource query Id.  Use `GET /v2/resource_query` API
               to look up the Resource query definition Ids  in your IBM Cloud account.
        :param bool force: (optional) Equivalent to -force options in the command
               line.
        :param bool propagate: (optional) Auto propagate the chaange or deletion to
               the dependent resources.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if query_id is None:
            raise ValueError('query_id must be provided')
        headers = {
            'force': force,
            'propagate': propagate
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_resources_query')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        path_param_keys = ['query_id']
        path_param_values = self.encode_path_vars(query_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/v2/resources_query/{query_id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request, **kwargs)
        return response

    #########################
    # settings-kms
    #########################


    def get_kms_settings(self,
        location: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Get KMS settings.

        Retrieve the KMS on the API endpoint that you have access. For example, if you use
        an API endpoint for a geography, such as North America, only Schematics resource
        that are created in `us-south` or `us-east` are retrieved.
        <h3>Authorization</h3>
         Schematics support generic authorization such as service access or platform
        access to the action ID and the resource group. For more information, about
        Schematics access and permissions, see [Schematics service access roles and
        required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str location: The location of the Resource.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `KMSSettings` object
        """

        if location is None:
            raise ValueError('location must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_kms_settings')
        headers.update(sdk_headers)

        params = {
            'location': location
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/settings/kms'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


    def update_kms_settings(self,
        *,
        location: str = None,
        encryption_scheme: str = None,
        resource_group: str = None,
        primary_crk: 'KMSSettingsPrimaryCrk' = None,
        secondary_crk: 'KMSSettingsSecondaryCrk' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Replace KMS settings.

        Replace or Update the KMS setting for your location, by using your private
        endpoint, `CRN`, primary `CRK`, and secondary `CRK`. **Note** you can update the
        KMS settings only once. For example, if you use an API endpoint for a geography,
        such as North America, only Schematics resource that are created in `us-south` or
        `us-east` are retrieved.
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to the action ID and the resource group. For more
        information, about Schematics access and permissions, see  [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str location: (optional) Location.
        :param str encryption_scheme: (optional) Encryption scheme.
        :param str resource_group: (optional) Resource group.
        :param KMSSettingsPrimaryCrk primary_crk: (optional) Primary CRK details.
        :param KMSSettingsSecondaryCrk secondary_crk: (optional) Secondary CRK
               details.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `KMSSettings` object
        """

        if primary_crk is not None:
            primary_crk = convert_model(primary_crk)
        if secondary_crk is not None:
            secondary_crk = convert_model(secondary_crk)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_kms_settings')
        headers.update(sdk_headers)

        data = {
            'location': location,
            'encryption_scheme': encryption_scheme,
            'resource_group': resource_group,
            'primary_crk': primary_crk,
            'secondary_crk': secondary_crk
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/settings/kms'
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request, **kwargs)
        return response


    def list_kms(self,
        encryption_scheme: str,
        location: str,
        *,
        resource_group: str = None,
        limit: int = None,
        sort: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        List KMS instances.

        Lists the KMS instances of your IBM Cloud account to find your Key Protect or
        Hyper Protect Crypto Services by using the location and encrypted scheme such as
        KYOK or BYOK.
        <h3>Authorization</h3> Schematics support generic authorization such as service
        access or platform access to the action ID and the resource group. For more
        information, about Schematics access and permissions, see  [Schematics service
        access roles and required
        permissions](https://cloud.ibm.com/docs/schematics?topic=schematics-access#access-roles).

        :param str encryption_scheme: The encryption scheme to be used.
        :param str location: The location of the Resource.
        :param str resource_group: (optional) The resource group (by default, fetch
               from all resource groups).
        :param int limit: (optional) The maximum number of items that you want to
               list. The number must be a positive integer between 1 and 2000. If no value
               is provided, 100 is used by default.
        :param str sort: (optional) Name of the field to sort-by;  Use the '.'
               character to delineate sub-resources and sub-fields (eg. owner.last_name).
               Prepend the field with '+' or '-', indicating 'ascending' or 'descending'
               (default is ascending)   Ignore unrecognized or unsupported sort field.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `KMSDiscovery` object
        """

        if encryption_scheme is None:
            raise ValueError('encryption_scheme must be provided')
        if location is None:
            raise ValueError('location must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_kms')
        headers.update(sdk_headers)

        params = {
            'encryption_scheme': encryption_scheme,
            'location': location,
            'resource_group': resource_group,
            'limit': limit,
            'sort': sort
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/v2/settings/kms_instances'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request, **kwargs)
        return response


class GetWorkspaceReadmeEnums:
    """
    Enums for get_workspace_readme parameters.
    """

    class Formatted(str, Enum):
        """
        The format of the readme file.  Value ''markdown'' will give markdown, otherwise
        html.
        """
        MARKDOWN = 'markdown'
        HTML = 'html'


class ListActionsEnums:
    """
    Enums for list_actions parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        IDS = 'ids'
        SUMMARY = 'summary'


class GetActionEnums:
    """
    Enums for get_action parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        SUMMARY = 'summary'
        DETAILED = 'detailed'


class ListJobsEnums:
    """
    Enums for list_jobs parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        IDS = 'ids'
        SUMMARY = 'summary'
    class Resource(str, Enum):
        """
        Name of the resource (workspace, actions or controls).
        """
        WORKSPACE = 'workspace'
        ACTION = 'action'
    class List(str, Enum):
        """
        list jobs.
        """
        ALL = 'all'


class GetJobEnums:
    """
    Enums for get_job parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        SUMMARY = 'summary'
        DETAILED = 'detailed'


class ListInventoriesEnums:
    """
    Enums for list_inventories parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        IDS = 'ids'
        SUMMARY = 'summary'


class ListResourceQueryEnums:
    """
    Enums for list_resource_query parameters.
    """

    class Profile(str, Enum):
        """
        Level of details returned by the get method.
        """
        IDS = 'ids'
        SUMMARY = 'summary'


##############################################################################
# Models
##############################################################################


class Action():
    """
    Complete Action details with user inputs and system generated data.

    :attr str name: (optional) The unique name of your action. The name can be up to
          128 characters long and can include alphanumeric characters, spaces, dashes, and
          underscores. **Example** you can use the name to stop action.
    :attr str description: (optional) Action description.
    :attr str location: (optional) List of locations supported by IBM Cloud
          Schematics service.  While creating your workspace or action, choose the right
          region, since it cannot be changed.  Note, this does not limit the location of
          the IBM Cloud resources, provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name for an action.  By
          default, action is created in default resource group.
    :attr List[str] tags: (optional) Action tags.
    :attr UserState user_state: (optional) User defined status of the Schematics
          object.
    :attr str source_readme_url: (optional) URL of the `README` file, for the source
          URL.
    :attr ExternalSource source: (optional) Source of templates, playbooks, or
          controls.
    :attr str source_type: (optional) Type of source for the Template.
    :attr str command_parameter: (optional) Schematics job command parameter
          (playbook-name).
    :attr str inventory: (optional) Target inventory record ID, used by the action
          or ansible playbook.
    :attr List[VariableData] credentials: (optional) credentials of the Action.
    :attr BastionResourceDefinition bastion: (optional) Describes a bastion
          resource.
    :attr VariableData bastion_credential: (optional) User editable variable data &
          system generated reference to value.
    :attr str targets_ini: (optional) Inventory of host and host group for the
          playbook in `INI` file format. For example, `"targets_ini": "[webserverhost]
           172.22.192.6
           [dbhost]
           172.22.192.5"`. For more information, about an inventory host group syntax, see
          [Inventory host
          groups](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-inventory-host-grps).
    :attr List[VariableData] inputs: (optional) Input variables for the Action.
    :attr List[VariableData] outputs: (optional) Output variables for the Action.
    :attr List[VariableData] settings: (optional) Environment variables for the
          Action.
    :attr str id: (optional) Action ID.
    :attr str crn: (optional) Action Cloud Resource Name.
    :attr str account: (optional) Action account ID.
    :attr datetime source_created_at: (optional) Action Playbook Source creation
          time.
    :attr str source_created_by: (optional) E-mail address of user who created the
          Action Playbook Source.
    :attr datetime source_updated_at: (optional) The action playbook updation time.
    :attr str source_updated_by: (optional) E-mail address of user who updated the
          action playbook source.
    :attr datetime created_at: (optional) Action creation time.
    :attr str created_by: (optional) E-mail address of the user who created an
          action.
    :attr datetime updated_at: (optional) Action updation time.
    :attr str updated_by: (optional) E-mail address of the user who updated an
          action.
    :attr ActionState state: (optional) Computed state of the Action.
    :attr List[str] playbook_names: (optional) Playbook names retrieved from the
          respository.
    :attr SystemLock sys_lock: (optional) System lock status.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 description: str = None,
                 location: str = None,
                 resource_group: str = None,
                 tags: List[str] = None,
                 user_state: 'UserState' = None,
                 source_readme_url: str = None,
                 source: 'ExternalSource' = None,
                 source_type: str = None,
                 command_parameter: str = None,
                 inventory: str = None,
                 credentials: List['VariableData'] = None,
                 bastion: 'BastionResourceDefinition' = None,
                 bastion_credential: 'VariableData' = None,
                 targets_ini: str = None,
                 inputs: List['VariableData'] = None,
                 outputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 id: str = None,
                 crn: str = None,
                 account: str = None,
                 source_created_at: datetime = None,
                 source_created_by: str = None,
                 source_updated_at: datetime = None,
                 source_updated_by: str = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 state: 'ActionState' = None,
                 playbook_names: List[str] = None,
                 sys_lock: 'SystemLock' = None) -> None:
        """
        Initialize a Action object.

        :param str name: (optional) The unique name of your action. The name can be
               up to 128 characters long and can include alphanumeric characters, spaces,
               dashes, and underscores. **Example** you can use the name to stop action.
        :param str description: (optional) Action description.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for an action.
               By default, action is created in default resource group.
        :param List[str] tags: (optional) Action tags.
        :param UserState user_state: (optional) User defined status of the
               Schematics object.
        :param str source_readme_url: (optional) URL of the `README` file, for the
               source URL.
        :param ExternalSource source: (optional) Source of templates, playbooks, or
               controls.
        :param str source_type: (optional) Type of source for the Template.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param str inventory: (optional) Target inventory record ID, used by the
               action or ansible playbook.
        :param List[VariableData] credentials: (optional) credentials of the
               Action.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param VariableData bastion_credential: (optional) User editable variable
               data & system generated reference to value.
        :param str targets_ini: (optional) Inventory of host and host group for the
               playbook in `INI` file format. For example, `"targets_ini":
               "[webserverhost]
                172.22.192.6
                [dbhost]
                172.22.192.5"`. For more information, about an inventory host group
               syntax, see [Inventory host
               groups](https://cloud.ibm.com/docs/schematics?topic=schematics-schematics-cli-reference#schematics-inventory-host-grps).
        :param List[VariableData] inputs: (optional) Input variables for the
               Action.
        :param List[VariableData] outputs: (optional) Output variables for the
               Action.
        :param List[VariableData] settings: (optional) Environment variables for
               the Action.
        :param ActionState state: (optional) Computed state of the Action.
        :param SystemLock sys_lock: (optional) System lock status.
        """
        self.name = name
        self.description = description
        self.location = location
        self.resource_group = resource_group
        self.tags = tags
        self.user_state = user_state
        self.source_readme_url = source_readme_url
        self.source = source
        self.source_type = source_type
        self.command_parameter = command_parameter
        self.inventory = inventory
        self.credentials = credentials
        self.bastion = bastion
        self.bastion_credential = bastion_credential
        self.targets_ini = targets_ini
        self.inputs = inputs
        self.outputs = outputs
        self.settings = settings
        self.id = id
        self.crn = crn
        self.account = account
        self.source_created_at = source_created_at
        self.source_created_by = source_created_by
        self.source_updated_at = source_updated_at
        self.source_updated_by = source_updated_by
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.state = state
        self.playbook_names = playbook_names
        self.sys_lock = sys_lock

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Action':
        """Initialize a Action object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'user_state' in _dict:
            args['user_state'] = UserState.from_dict(_dict.get('user_state'))
        if 'source_readme_url' in _dict:
            args['source_readme_url'] = _dict.get('source_readme_url')
        if 'source' in _dict:
            args['source'] = ExternalSource.from_dict(_dict.get('source'))
        if 'source_type' in _dict:
            args['source_type'] = _dict.get('source_type')
        if 'command_parameter' in _dict:
            args['command_parameter'] = _dict.get('command_parameter')
        if 'inventory' in _dict:
            args['inventory'] = _dict.get('inventory')
        if 'credentials' in _dict:
            args['credentials'] = [VariableData.from_dict(x) for x in _dict.get('credentials')]
        if 'bastion' in _dict:
            args['bastion'] = BastionResourceDefinition.from_dict(_dict.get('bastion'))
        if 'bastion_credential' in _dict:
            args['bastion_credential'] = VariableData.from_dict(_dict.get('bastion_credential'))
        if 'targets_ini' in _dict:
            args['targets_ini'] = _dict.get('targets_ini')
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'outputs' in _dict:
            args['outputs'] = [VariableData.from_dict(x) for x in _dict.get('outputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'account' in _dict:
            args['account'] = _dict.get('account')
        if 'source_created_at' in _dict:
            args['source_created_at'] = string_to_datetime(_dict.get('source_created_at'))
        if 'source_created_by' in _dict:
            args['source_created_by'] = _dict.get('source_created_by')
        if 'source_updated_at' in _dict:
            args['source_updated_at'] = string_to_datetime(_dict.get('source_updated_at'))
        if 'source_updated_by' in _dict:
            args['source_updated_by'] = _dict.get('source_updated_by')
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'state' in _dict:
            args['state'] = ActionState.from_dict(_dict.get('state'))
        if 'playbook_names' in _dict:
            args['playbook_names'] = _dict.get('playbook_names')
        if 'sys_lock' in _dict:
            args['sys_lock'] = SystemLock.from_dict(_dict.get('sys_lock'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Action object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'user_state') and self.user_state is not None:
            _dict['user_state'] = self.user_state.to_dict()
        if hasattr(self, 'source_readme_url') and self.source_readme_url is not None:
            _dict['source_readme_url'] = self.source_readme_url
        if hasattr(self, 'source') and self.source is not None:
            _dict['source'] = self.source.to_dict()
        if hasattr(self, 'source_type') and self.source_type is not None:
            _dict['source_type'] = self.source_type
        if hasattr(self, 'command_parameter') and self.command_parameter is not None:
            _dict['command_parameter'] = self.command_parameter
        if hasattr(self, 'inventory') and self.inventory is not None:
            _dict['inventory'] = self.inventory
        if hasattr(self, 'credentials') and self.credentials is not None:
            _dict['credentials'] = [x.to_dict() for x in self.credentials]
        if hasattr(self, 'bastion') and self.bastion is not None:
            _dict['bastion'] = self.bastion.to_dict()
        if hasattr(self, 'bastion_credential') and self.bastion_credential is not None:
            _dict['bastion_credential'] = self.bastion_credential.to_dict()
        if hasattr(self, 'targets_ini') and self.targets_ini is not None:
            _dict['targets_ini'] = self.targets_ini
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'outputs') and self.outputs is not None:
            _dict['outputs'] = [x.to_dict() for x in self.outputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'crn') and getattr(self, 'crn') is not None:
            _dict['crn'] = getattr(self, 'crn')
        if hasattr(self, 'account') and getattr(self, 'account') is not None:
            _dict['account'] = getattr(self, 'account')
        if hasattr(self, 'source_created_at') and getattr(self, 'source_created_at') is not None:
            _dict['source_created_at'] = datetime_to_string(getattr(self, 'source_created_at'))
        if hasattr(self, 'source_created_by') and getattr(self, 'source_created_by') is not None:
            _dict['source_created_by'] = getattr(self, 'source_created_by')
        if hasattr(self, 'source_updated_at') and getattr(self, 'source_updated_at') is not None:
            _dict['source_updated_at'] = datetime_to_string(getattr(self, 'source_updated_at'))
        if hasattr(self, 'source_updated_by') and getattr(self, 'source_updated_by') is not None:
            _dict['source_updated_by'] = getattr(self, 'source_updated_by')
        if hasattr(self, 'created_at') and getattr(self, 'created_at') is not None:
            _dict['created_at'] = datetime_to_string(getattr(self, 'created_at'))
        if hasattr(self, 'created_by') and getattr(self, 'created_by') is not None:
            _dict['created_by'] = getattr(self, 'created_by')
        if hasattr(self, 'updated_at') and getattr(self, 'updated_at') is not None:
            _dict['updated_at'] = datetime_to_string(getattr(self, 'updated_at'))
        if hasattr(self, 'updated_by') and getattr(self, 'updated_by') is not None:
            _dict['updated_by'] = getattr(self, 'updated_by')
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state.to_dict()
        if hasattr(self, 'playbook_names') and getattr(self, 'playbook_names') is not None:
            _dict['playbook_names'] = getattr(self, 'playbook_names')
        if hasattr(self, 'sys_lock') and self.sys_lock is not None:
            _dict['sys_lock'] = self.sys_lock.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Action object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Action') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Action') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LocationEnum(str, Enum):
        """
        List of locations supported by IBM Cloud Schematics service.  While creating your
        workspace or action, choose the right region, since it cannot be changed.  Note,
        this does not limit the location of the IBM Cloud resources, provisioned using
        Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


    class SourceTypeEnum(str, Enum):
        """
        Type of source for the Template.
        """
        LOCAL = 'local'
        GIT_HUB = 'git_hub'
        GIT_HUB_ENTERPRISE = 'git_hub_enterprise'
        GIT_LAB = 'git_lab'
        IBM_GIT_LAB = 'ibm_git_lab'
        IBM_CLOUD_CATALOG = 'ibm_cloud_catalog'
        EXTERNAL_SCM = 'external_scm'
        COS_BUCKET = 'cos_bucket'


class ActionList():
    """
    List of Action definition response.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[ActionLite] actions: (optional) List of action records.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 actions: List['ActionLite'] = None) -> None:
        """
        Initialize a ActionList object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[ActionLite] actions: (optional) List of action records.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.actions = actions

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionList':
        """Initialize a ActionList object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in ActionList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in ActionList JSON')
        if 'actions' in _dict:
            args['actions'] = [ActionLite.from_dict(x) for x in _dict.get('actions')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'actions') and self.actions is not None:
            _dict['actions'] = [x.to_dict() for x in self.actions]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ActionLite():
    """
    Action summary profile with user inputs and system generated data.

    :attr str name: (optional) Action name (unique for an account).
    :attr str description: (optional) Action description.
    :attr str id: (optional) Action Id.
    :attr str crn: (optional) Action Cloud Resource Name.
    :attr str location: (optional) List of locations supported by IBM Cloud
          Schematics service.  While creating your workspace or action, choose the right
          region, since it cannot be changed.  Note, this does not limit the location of
          the IBM Cloud resources, provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name for the Action.  By
          default, Action will be created in Default Resource Group.
    :attr str namespace: (optional) name of the namespace.
    :attr List[str] tags: (optional) Action tags.
    :attr str playbook_name: (optional) Name of the selected playbook.
    :attr UserState user_state: (optional) User defined status of the Schematics
          object.
    :attr ActionLiteState state: (optional) Computed state of the Action.
    :attr SystemLock sys_lock: (optional) System lock status.
    :attr datetime created_at: (optional) Action creation time.
    :attr str created_by: (optional) Email address of user who created the action.
    :attr datetime updated_at: (optional) Action updation time.
    :attr str updated_by: (optional) Email address of user who updated the action.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 description: str = None,
                 id: str = None,
                 crn: str = None,
                 location: str = None,
                 resource_group: str = None,
                 namespace: str = None,
                 tags: List[str] = None,
                 playbook_name: str = None,
                 user_state: 'UserState' = None,
                 state: 'ActionLiteState' = None,
                 sys_lock: 'SystemLock' = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None) -> None:
        """
        Initialize a ActionLite object.

        :param str name: (optional) Action name (unique for an account).
        :param str description: (optional) Action description.
        :param str id: (optional) Action Id.
        :param str crn: (optional) Action Cloud Resource Name.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Action.
               By default, Action will be created in Default Resource Group.
        :param str namespace: (optional) name of the namespace.
        :param List[str] tags: (optional) Action tags.
        :param str playbook_name: (optional) Name of the selected playbook.
        :param UserState user_state: (optional) User defined status of the
               Schematics object.
        :param ActionLiteState state: (optional) Computed state of the Action.
        :param SystemLock sys_lock: (optional) System lock status.
        :param datetime created_at: (optional) Action creation time.
        :param str created_by: (optional) Email address of user who created the
               action.
        :param datetime updated_at: (optional) Action updation time.
        :param str updated_by: (optional) Email address of user who updated the
               action.
        """
        self.name = name
        self.description = description
        self.id = id
        self.crn = crn
        self.location = location
        self.resource_group = resource_group
        self.namespace = namespace
        self.tags = tags
        self.playbook_name = playbook_name
        self.user_state = user_state
        self.state = state
        self.sys_lock = sys_lock
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionLite':
        """Initialize a ActionLite object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'namespace' in _dict:
            args['namespace'] = _dict.get('namespace')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'playbook_name' in _dict:
            args['playbook_name'] = _dict.get('playbook_name')
        if 'user_state' in _dict:
            args['user_state'] = UserState.from_dict(_dict.get('user_state'))
        if 'state' in _dict:
            args['state'] = ActionLiteState.from_dict(_dict.get('state'))
        if 'sys_lock' in _dict:
            args['sys_lock'] = SystemLock.from_dict(_dict.get('sys_lock'))
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionLite object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['crn'] = self.crn
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'namespace') and self.namespace is not None:
            _dict['namespace'] = self.namespace
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'playbook_name') and self.playbook_name is not None:
            _dict['playbook_name'] = self.playbook_name
        if hasattr(self, 'user_state') and self.user_state is not None:
            _dict['user_state'] = self.user_state.to_dict()
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state.to_dict()
        if hasattr(self, 'sys_lock') and self.sys_lock is not None:
            _dict['sys_lock'] = self.sys_lock.to_dict()
        if hasattr(self, 'created_at') and self.created_at is not None:
            _dict['created_at'] = datetime_to_string(self.created_at)
        if hasattr(self, 'created_by') and self.created_by is not None:
            _dict['created_by'] = self.created_by
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        if hasattr(self, 'updated_by') and self.updated_by is not None:
            _dict['updated_by'] = self.updated_by
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionLite object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionLite') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionLite') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LocationEnum(str, Enum):
        """
        List of locations supported by IBM Cloud Schematics service.  While creating your
        workspace or action, choose the right region, since it cannot be changed.  Note,
        this does not limit the location of the IBM Cloud resources, provisioned using
        Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


class ActionLiteState():
    """
    Computed state of the Action.

    :attr str status_code: (optional) Status of automation (workspace or action).
    :attr str status_message: (optional) Automation status message - to be displayed
          along with the status_code.
    """

    def __init__(self,
                 *,
                 status_code: str = None,
                 status_message: str = None) -> None:
        """
        Initialize a ActionLiteState object.

        :param str status_code: (optional) Status of automation (workspace or
               action).
        :param str status_message: (optional) Automation status message - to be
               displayed along with the status_code.
        """
        self.status_code = status_code
        self.status_message = status_message

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionLiteState':
        """Initialize a ActionLiteState object from a json dictionary."""
        args = {}
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionLiteState object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionLiteState object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionLiteState') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionLiteState') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of automation (workspace or action).
        """
        NORMAL = 'normal'
        PENDING = 'pending'
        DISABLED = 'disabled'
        CRITICAL = 'critical'


class ActionState():
    """
    Computed state of the Action.

    :attr str status_code: (optional) Status of automation (workspace or action).
    :attr str status_job_id: (optional) Job id reference for this status.
    :attr str status_message: (optional) Automation status message - to be displayed
          along with the status_code.
    """

    def __init__(self,
                 *,
                 status_code: str = None,
                 status_job_id: str = None,
                 status_message: str = None) -> None:
        """
        Initialize a ActionState object.

        :param str status_code: (optional) Status of automation (workspace or
               action).
        :param str status_job_id: (optional) Job id reference for this status.
        :param str status_message: (optional) Automation status message - to be
               displayed along with the status_code.
        """
        self.status_code = status_code
        self.status_job_id = status_job_id
        self.status_message = status_message

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionState':
        """Initialize a ActionState object from a json dictionary."""
        args = {}
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_job_id' in _dict:
            args['status_job_id'] = _dict.get('status_job_id')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionState object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_job_id') and self.status_job_id is not None:
            _dict['status_job_id'] = self.status_job_id
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionState object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionState') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionState') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of automation (workspace or action).
        """
        NORMAL = 'normal'
        PENDING = 'pending'
        DISABLED = 'disabled'
        CRITICAL = 'critical'


class BastionResourceDefinition():
    """
    Describes a bastion resource.

    :attr str name: (optional) Bastion Name(Unique).
    :attr str host: (optional) Reference to the Inventory resource definition.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 host: str = None) -> None:
        """
        Initialize a BastionResourceDefinition object.

        :param str name: (optional) Bastion Name(Unique).
        :param str host: (optional) Reference to the Inventory resource definition.
        """
        self.name = name
        self.host = host

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'BastionResourceDefinition':
        """Initialize a BastionResourceDefinition object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'host' in _dict:
            args['host'] = _dict.get('host')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a BastionResourceDefinition object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'host') and self.host is not None:
            _dict['host'] = self.host
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this BastionResourceDefinition object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'BastionResourceDefinition') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'BastionResourceDefinition') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CatalogRef():
    """
    Information about the software template that you chose from the IBM Cloud catalog.
    This information is returned for IBM Cloud catalog offerings only.

    :attr bool dry_run: (optional) Dry run.
    :attr str owning_account: (optional) Owning account ID of the catalog.
    :attr str item_icon_url: (optional) The URL to the icon of the software template
          in the IBM Cloud catalog.
    :attr str item_id: (optional) The ID of the software template that you chose to
          install from the IBM Cloud catalog. This software is provisioned with
          Schematics.
    :attr str item_name: (optional) The name of the software that you chose to
          install from the IBM Cloud catalog.
    :attr str item_readme_url: (optional) The URL to the readme file of the software
          template in the IBM Cloud catalog.
    :attr str item_url: (optional) The URL to the software template in the IBM Cloud
          catalog.
    :attr str launch_url: (optional) The URL to the dashboard to access your
          software.
    :attr str offering_version: (optional) The version of the software template that
          you chose to install from the IBM Cloud catalog.
    """

    def __init__(self,
                 *,
                 dry_run: bool = None,
                 owning_account: str = None,
                 item_icon_url: str = None,
                 item_id: str = None,
                 item_name: str = None,
                 item_readme_url: str = None,
                 item_url: str = None,
                 launch_url: str = None,
                 offering_version: str = None) -> None:
        """
        Initialize a CatalogRef object.

        :param bool dry_run: (optional) Dry run.
        :param str owning_account: (optional) Owning account ID of the catalog.
        :param str item_icon_url: (optional) The URL to the icon of the software
               template in the IBM Cloud catalog.
        :param str item_id: (optional) The ID of the software template that you
               chose to install from the IBM Cloud catalog. This software is provisioned
               with Schematics.
        :param str item_name: (optional) The name of the software that you chose to
               install from the IBM Cloud catalog.
        :param str item_readme_url: (optional) The URL to the readme file of the
               software template in the IBM Cloud catalog.
        :param str item_url: (optional) The URL to the software template in the IBM
               Cloud catalog.
        :param str launch_url: (optional) The URL to the dashboard to access your
               software.
        :param str offering_version: (optional) The version of the software
               template that you chose to install from the IBM Cloud catalog.
        """
        self.dry_run = dry_run
        self.owning_account = owning_account
        self.item_icon_url = item_icon_url
        self.item_id = item_id
        self.item_name = item_name
        self.item_readme_url = item_readme_url
        self.item_url = item_url
        self.launch_url = launch_url
        self.offering_version = offering_version

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CatalogRef':
        """Initialize a CatalogRef object from a json dictionary."""
        args = {}
        if 'dry_run' in _dict:
            args['dry_run'] = _dict.get('dry_run')
        if 'owning_account' in _dict:
            args['owning_account'] = _dict.get('owning_account')
        if 'item_icon_url' in _dict:
            args['item_icon_url'] = _dict.get('item_icon_url')
        if 'item_id' in _dict:
            args['item_id'] = _dict.get('item_id')
        if 'item_name' in _dict:
            args['item_name'] = _dict.get('item_name')
        if 'item_readme_url' in _dict:
            args['item_readme_url'] = _dict.get('item_readme_url')
        if 'item_url' in _dict:
            args['item_url'] = _dict.get('item_url')
        if 'launch_url' in _dict:
            args['launch_url'] = _dict.get('launch_url')
        if 'offering_version' in _dict:
            args['offering_version'] = _dict.get('offering_version')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CatalogRef object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'dry_run') and self.dry_run is not None:
            _dict['dry_run'] = self.dry_run
        if hasattr(self, 'owning_account') and self.owning_account is not None:
            _dict['owning_account'] = self.owning_account
        if hasattr(self, 'item_icon_url') and self.item_icon_url is not None:
            _dict['item_icon_url'] = self.item_icon_url
        if hasattr(self, 'item_id') and self.item_id is not None:
            _dict['item_id'] = self.item_id
        if hasattr(self, 'item_name') and self.item_name is not None:
            _dict['item_name'] = self.item_name
        if hasattr(self, 'item_readme_url') and self.item_readme_url is not None:
            _dict['item_readme_url'] = self.item_readme_url
        if hasattr(self, 'item_url') and self.item_url is not None:
            _dict['item_url'] = self.item_url
        if hasattr(self, 'launch_url') and self.launch_url is not None:
            _dict['launch_url'] = self.launch_url
        if hasattr(self, 'offering_version') and self.offering_version is not None:
            _dict['offering_version'] = self.offering_version
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CatalogRef object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CatalogRef') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CatalogRef') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class EnvVariableResponse():
    """
    List of environment values.

    :attr bool hidden: (optional) Environment variable is hidden.
    :attr str name: (optional) Environment variable name.
    :attr bool secure: (optional) Environment variable is secure.
    :attr str value: (optional) Value for environment variable.
    """

    def __init__(self,
                 *,
                 hidden: bool = None,
                 name: str = None,
                 secure: bool = None,
                 value: str = None) -> None:
        """
        Initialize a EnvVariableResponse object.

        :param bool hidden: (optional) Environment variable is hidden.
        :param str name: (optional) Environment variable name.
        :param bool secure: (optional) Environment variable is secure.
        :param str value: (optional) Value for environment variable.
        """
        self.hidden = hidden
        self.name = name
        self.secure = secure
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'EnvVariableResponse':
        """Initialize a EnvVariableResponse object from a json dictionary."""
        args = {}
        if 'hidden' in _dict:
            args['hidden'] = _dict.get('hidden')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a EnvVariableResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'hidden') and self.hidden is not None:
            _dict['hidden'] = self.hidden
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this EnvVariableResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'EnvVariableResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'EnvVariableResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ExternalSource():
    """
    Source of templates, playbooks, or controls.

    :attr str source_type: Type of source for the Template.
    :attr ExternalSourceGit git: (optional) Connection details to Git source.
    :attr ExternalSourceCatalog catalog: (optional) Connection details to IBM Cloud
          Catalog source.
    :attr ExternalSourceCosBucket cos_bucket: (optional) Connection details to a IBM
          Cloud Object Storage bucket.
    """

    def __init__(self,
                 source_type: str,
                 *,
                 git: 'ExternalSourceGit' = None,
                 catalog: 'ExternalSourceCatalog' = None,
                 cos_bucket: 'ExternalSourceCosBucket' = None) -> None:
        """
        Initialize a ExternalSource object.

        :param str source_type: Type of source for the Template.
        :param ExternalSourceGit git: (optional) Connection details to Git source.
        :param ExternalSourceCatalog catalog: (optional) Connection details to IBM
               Cloud Catalog source.
        :param ExternalSourceCosBucket cos_bucket: (optional) Connection details to
               a IBM Cloud Object Storage bucket.
        """
        self.source_type = source_type
        self.git = git
        self.catalog = catalog
        self.cos_bucket = cos_bucket

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ExternalSource':
        """Initialize a ExternalSource object from a json dictionary."""
        args = {}
        if 'source_type' in _dict:
            args['source_type'] = _dict.get('source_type')
        else:
            raise ValueError('Required property \'source_type\' not present in ExternalSource JSON')
        if 'git' in _dict:
            args['git'] = ExternalSourceGit.from_dict(_dict.get('git'))
        if 'catalog' in _dict:
            args['catalog'] = ExternalSourceCatalog.from_dict(_dict.get('catalog'))
        if 'cos_bucket' in _dict:
            args['cos_bucket'] = ExternalSourceCosBucket.from_dict(_dict.get('cos_bucket'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ExternalSource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'source_type') and self.source_type is not None:
            _dict['source_type'] = self.source_type
        if hasattr(self, 'git') and self.git is not None:
            _dict['git'] = self.git.to_dict()
        if hasattr(self, 'catalog') and self.catalog is not None:
            _dict['catalog'] = self.catalog.to_dict()
        if hasattr(self, 'cos_bucket') and self.cos_bucket is not None:
            _dict['cos_bucket'] = self.cos_bucket.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ExternalSource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ExternalSource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ExternalSource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class SourceTypeEnum(str, Enum):
        """
        Type of source for the Template.
        """
        LOCAL = 'local'
        GIT_HUB = 'git_hub'
        GIT_HUB_ENTERPRISE = 'git_hub_enterprise'
        GIT_LAB = 'git_lab'
        IBM_GIT_LAB = 'ibm_git_lab'
        IBM_CLOUD_CATALOG = 'ibm_cloud_catalog'
        EXTERNAL_SCM = 'external_scm'
        COS_BUCKET = 'cos_bucket'


class ExternalSourceCatalog():
    """
    Connection details to IBM Cloud Catalog source.

    :attr str catalog_name: (optional) name of the private catalog.
    :attr str offering_name: (optional) Name of the offering in the IBM Catalog.
    :attr str offering_version: (optional) Version string of the offering in the IBM
          Catalog.
    :attr str offering_kind: (optional) Type of the offering, in the IBM Catalog.
    :attr str offering_id: (optional) Id of the offering the IBM Catalog.
    :attr str offering_version_id: (optional) Id of the offering version the IBM
          Catalog.
    :attr str offering_repo_url: (optional) Repo Url of the offering, in the IBM
          Catalog.
    """

    def __init__(self,
                 *,
                 catalog_name: str = None,
                 offering_name: str = None,
                 offering_version: str = None,
                 offering_kind: str = None,
                 offering_id: str = None,
                 offering_version_id: str = None,
                 offering_repo_url: str = None) -> None:
        """
        Initialize a ExternalSourceCatalog object.

        :param str catalog_name: (optional) name of the private catalog.
        :param str offering_name: (optional) Name of the offering in the IBM
               Catalog.
        :param str offering_version: (optional) Version string of the offering in
               the IBM Catalog.
        :param str offering_kind: (optional) Type of the offering, in the IBM
               Catalog.
        :param str offering_id: (optional) Id of the offering the IBM Catalog.
        :param str offering_version_id: (optional) Id of the offering version the
               IBM Catalog.
        :param str offering_repo_url: (optional) Repo Url of the offering, in the
               IBM Catalog.
        """
        self.catalog_name = catalog_name
        self.offering_name = offering_name
        self.offering_version = offering_version
        self.offering_kind = offering_kind
        self.offering_id = offering_id
        self.offering_version_id = offering_version_id
        self.offering_repo_url = offering_repo_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ExternalSourceCatalog':
        """Initialize a ExternalSourceCatalog object from a json dictionary."""
        args = {}
        if 'catalog_name' in _dict:
            args['catalog_name'] = _dict.get('catalog_name')
        if 'offering_name' in _dict:
            args['offering_name'] = _dict.get('offering_name')
        if 'offering_version' in _dict:
            args['offering_version'] = _dict.get('offering_version')
        if 'offering_kind' in _dict:
            args['offering_kind'] = _dict.get('offering_kind')
        if 'offering_id' in _dict:
            args['offering_id'] = _dict.get('offering_id')
        if 'offering_version_id' in _dict:
            args['offering_version_id'] = _dict.get('offering_version_id')
        if 'offering_repo_url' in _dict:
            args['offering_repo_url'] = _dict.get('offering_repo_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ExternalSourceCatalog object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'catalog_name') and self.catalog_name is not None:
            _dict['catalog_name'] = self.catalog_name
        if hasattr(self, 'offering_name') and self.offering_name is not None:
            _dict['offering_name'] = self.offering_name
        if hasattr(self, 'offering_version') and self.offering_version is not None:
            _dict['offering_version'] = self.offering_version
        if hasattr(self, 'offering_kind') and self.offering_kind is not None:
            _dict['offering_kind'] = self.offering_kind
        if hasattr(self, 'offering_id') and self.offering_id is not None:
            _dict['offering_id'] = self.offering_id
        if hasattr(self, 'offering_version_id') and self.offering_version_id is not None:
            _dict['offering_version_id'] = self.offering_version_id
        if hasattr(self, 'offering_repo_url') and self.offering_repo_url is not None:
            _dict['offering_repo_url'] = self.offering_repo_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ExternalSourceCatalog object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ExternalSourceCatalog') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ExternalSourceCatalog') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ExternalSourceCosBucket():
    """
    Connection details to a IBM Cloud Object Storage bucket.

    :attr str cos_bucket_url: (optional) COS Bucket Url.
    """

    def __init__(self,
                 *,
                 cos_bucket_url: str = None) -> None:
        """
        Initialize a ExternalSourceCosBucket object.

        :param str cos_bucket_url: (optional) COS Bucket Url.
        """
        self.cos_bucket_url = cos_bucket_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ExternalSourceCosBucket':
        """Initialize a ExternalSourceCosBucket object from a json dictionary."""
        args = {}
        if 'cos_bucket_url' in _dict:
            args['cos_bucket_url'] = _dict.get('cos_bucket_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ExternalSourceCosBucket object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cos_bucket_url') and self.cos_bucket_url is not None:
            _dict['cos_bucket_url'] = self.cos_bucket_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ExternalSourceCosBucket object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ExternalSourceCosBucket') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ExternalSourceCosBucket') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ExternalSourceGit():
    """
    Connection details to Git source.

    :attr str computed_git_repo_url: (optional) The Complete URL which is computed
          by git_repo_url, git_repo_folder and branch.
    :attr str git_repo_url: (optional) URL to the GIT Repo that can be used to clone
          the template.
    :attr str git_token: (optional) Personal Access Token to connect to Git URLs.
    :attr str git_repo_folder: (optional) Name of the folder in the Git Repo, that
          contains the template.
    :attr str git_release: (optional) Name of the release tag, used to fetch the Git
          Repo.
    :attr str git_branch: (optional) Name of the branch, used to fetch the Git Repo.
    """

    def __init__(self,
                 *,
                 computed_git_repo_url: str = None,
                 git_repo_url: str = None,
                 git_token: str = None,
                 git_repo_folder: str = None,
                 git_release: str = None,
                 git_branch: str = None) -> None:
        """
        Initialize a ExternalSourceGit object.

        :param str computed_git_repo_url: (optional) The Complete URL which is
               computed by git_repo_url, git_repo_folder and branch.
        :param str git_repo_url: (optional) URL to the GIT Repo that can be used to
               clone the template.
        :param str git_token: (optional) Personal Access Token to connect to Git
               URLs.
        :param str git_repo_folder: (optional) Name of the folder in the Git Repo,
               that contains the template.
        :param str git_release: (optional) Name of the release tag, used to fetch
               the Git Repo.
        :param str git_branch: (optional) Name of the branch, used to fetch the Git
               Repo.
        """
        self.computed_git_repo_url = computed_git_repo_url
        self.git_repo_url = git_repo_url
        self.git_token = git_token
        self.git_repo_folder = git_repo_folder
        self.git_release = git_release
        self.git_branch = git_branch

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ExternalSourceGit':
        """Initialize a ExternalSourceGit object from a json dictionary."""
        args = {}
        if 'computed_git_repo_url' in _dict:
            args['computed_git_repo_url'] = _dict.get('computed_git_repo_url')
        if 'git_repo_url' in _dict:
            args['git_repo_url'] = _dict.get('git_repo_url')
        if 'git_token' in _dict:
            args['git_token'] = _dict.get('git_token')
        if 'git_repo_folder' in _dict:
            args['git_repo_folder'] = _dict.get('git_repo_folder')
        if 'git_release' in _dict:
            args['git_release'] = _dict.get('git_release')
        if 'git_branch' in _dict:
            args['git_branch'] = _dict.get('git_branch')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ExternalSourceGit object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'computed_git_repo_url') and self.computed_git_repo_url is not None:
            _dict['computed_git_repo_url'] = self.computed_git_repo_url
        if hasattr(self, 'git_repo_url') and self.git_repo_url is not None:
            _dict['git_repo_url'] = self.git_repo_url
        if hasattr(self, 'git_token') and self.git_token is not None:
            _dict['git_token'] = self.git_token
        if hasattr(self, 'git_repo_folder') and self.git_repo_folder is not None:
            _dict['git_repo_folder'] = self.git_repo_folder
        if hasattr(self, 'git_release') and self.git_release is not None:
            _dict['git_release'] = self.git_release
        if hasattr(self, 'git_branch') and self.git_branch is not None:
            _dict['git_branch'] = self.git_branch
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ExternalSourceGit object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ExternalSourceGit') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ExternalSourceGit') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class InventoryResourceRecord():
    """
    Complete inventory resource details with user inputs and system generated data.

    :attr str name: (optional) The unique name of your Inventory.  The name can be
          up to 128 characters long and can include alphanumeric  characters, spaces,
          dashes, and underscores.
    :attr str id: (optional) Inventory id.
    :attr str description: (optional) The description of your Inventory.  The
          description can be up to 2048 characters long in size.
    :attr str location: (optional) List of locations supported by IBM Cloud
          Schematics service.  While creating your workspace or action, choose the right
          region, since it cannot be changed.  Note, this does not limit the location of
          the IBM Cloud resources, provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name for the Inventory
          definition.  By default, Inventory will be created in Default Resource Group.
    :attr datetime created_at: (optional) Inventory creation time.
    :attr str created_by: (optional) Email address of user who created the
          Inventory.
    :attr datetime updated_at: (optional) Inventory updation time.
    :attr str updated_by: (optional) Email address of user who updated the
          Inventory.
    :attr str inventories_ini: (optional) Input inventory of host and host group for
          the playbook,  in the .ini file format.
    :attr List[str] resource_queries: (optional) Input resource queries that is used
          to dynamically generate  the inventory of host and host group for the playbook.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 id: str = None,
                 description: str = None,
                 location: str = None,
                 resource_group: str = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 inventories_ini: str = None,
                 resource_queries: List[str] = None) -> None:
        """
        Initialize a InventoryResourceRecord object.

        :param str name: (optional) The unique name of your Inventory.  The name
               can be up to 128 characters long and can include alphanumeric  characters,
               spaces, dashes, and underscores.
        :param str description: (optional) The description of your Inventory.  The
               description can be up to 2048 characters long in size.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name for the Inventory
               definition.  By default, Inventory will be created in Default Resource
               Group.
        :param str inventories_ini: (optional) Input inventory of host and host
               group for the playbook,  in the .ini file format.
        :param List[str] resource_queries: (optional) Input resource queries that
               is used to dynamically generate  the inventory of host and host group for
               the playbook.
        """
        self.name = name
        self.id = id
        self.description = description
        self.location = location
        self.resource_group = resource_group
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.inventories_ini = inventories_ini
        self.resource_queries = resource_queries

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'InventoryResourceRecord':
        """Initialize a InventoryResourceRecord object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'inventories_ini' in _dict:
            args['inventories_ini'] = _dict.get('inventories_ini')
        if 'resource_queries' in _dict:
            args['resource_queries'] = _dict.get('resource_queries')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a InventoryResourceRecord object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'created_at') and getattr(self, 'created_at') is not None:
            _dict['created_at'] = datetime_to_string(getattr(self, 'created_at'))
        if hasattr(self, 'created_by') and getattr(self, 'created_by') is not None:
            _dict['created_by'] = getattr(self, 'created_by')
        if hasattr(self, 'updated_at') and getattr(self, 'updated_at') is not None:
            _dict['updated_at'] = datetime_to_string(getattr(self, 'updated_at'))
        if hasattr(self, 'updated_by') and getattr(self, 'updated_by') is not None:
            _dict['updated_by'] = getattr(self, 'updated_by')
        if hasattr(self, 'inventories_ini') and self.inventories_ini is not None:
            _dict['inventories_ini'] = self.inventories_ini
        if hasattr(self, 'resource_queries') and self.resource_queries is not None:
            _dict['resource_queries'] = self.resource_queries
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this InventoryResourceRecord object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'InventoryResourceRecord') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'InventoryResourceRecord') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LocationEnum(str, Enum):
        """
        List of locations supported by IBM Cloud Schematics service.  While creating your
        workspace or action, choose the right region, since it cannot be changed.  Note,
        this does not limit the location of the IBM Cloud resources, provisioned using
        Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


class InventoryResourceRecordList():
    """
    List of Inventory definition records.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[InventoryResourceRecord] inventories: (optional) List of inventory
          definition records.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 inventories: List['InventoryResourceRecord'] = None) -> None:
        """
        Initialize a InventoryResourceRecordList object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[InventoryResourceRecord] inventories: (optional) List of
               inventory definition records.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.inventories = inventories

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'InventoryResourceRecordList':
        """Initialize a InventoryResourceRecordList object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in InventoryResourceRecordList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in InventoryResourceRecordList JSON')
        if 'inventories' in _dict:
            args['inventories'] = [InventoryResourceRecord.from_dict(x) for x in _dict.get('inventories')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a InventoryResourceRecordList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'inventories') and self.inventories is not None:
            _dict['inventories'] = [x.to_dict() for x in self.inventories]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this InventoryResourceRecordList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'InventoryResourceRecordList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'InventoryResourceRecordList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Job():
    """
    Complete Job with user inputs and system generated data.

    :attr str command_object: (optional) Name of the Schematics automation resource.
    :attr str command_object_id: (optional) Job command object id (workspace-id,
          action-id).
    :attr str command_name: (optional) Schematics job command name.
    :attr str command_parameter: (optional) Schematics job command parameter
          (playbook-name).
    :attr List[str] command_options: (optional) Command line options for the
          command.
    :attr List[VariableData] inputs: (optional) Job inputs used by Action or
          Workspace.
    :attr List[VariableData] settings: (optional) Environment variables used by the
          Job while performing Action or Workspace.
    :attr List[str] tags: (optional) User defined tags, while running the job.
    :attr str id: (optional) Job ID.
    :attr str name: (optional) Job name, uniquely derived from the related Workspace
          or Action.
    :attr str description: (optional) The description of your job is derived from
          the related action or workspace.  The description can be up to 2048 characters
          long in size.
    :attr str location: (optional) List of locations supported by IBM Cloud
          Schematics service.  While creating your workspace or action, choose the right
          region, since it cannot be changed.  Note, this does not limit the location of
          the IBM Cloud resources, provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name derived from the
          related Workspace or Action.
    :attr datetime submitted_at: (optional) Job submission time.
    :attr str submitted_by: (optional) Email address of user who submitted the job.
    :attr datetime start_at: (optional) Job start time.
    :attr datetime end_at: (optional) Job end time.
    :attr str duration: (optional) Duration of job execution; example 40 sec.
    :attr JobStatus status: (optional) Job Status.
    :attr JobData data: (optional) Job data.
    :attr BastionResourceDefinition bastion: (optional) Describes a bastion
          resource.
    :attr JobLogSummary log_summary: (optional) Job log summary record.
    :attr str log_store_url: (optional) Job log store URL.
    :attr str state_store_url: (optional) Job state store URL.
    :attr str results_url: (optional) Job results store URL.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 command_object: str = None,
                 command_object_id: str = None,
                 command_name: str = None,
                 command_parameter: str = None,
                 command_options: List[str] = None,
                 inputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 tags: List[str] = None,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 location: str = None,
                 resource_group: str = None,
                 submitted_at: datetime = None,
                 submitted_by: str = None,
                 start_at: datetime = None,
                 end_at: datetime = None,
                 duration: str = None,
                 status: 'JobStatus' = None,
                 data: 'JobData' = None,
                 bastion: 'BastionResourceDefinition' = None,
                 log_summary: 'JobLogSummary' = None,
                 log_store_url: str = None,
                 state_store_url: str = None,
                 results_url: str = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a Job object.

        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_id: (optional) Job command object id
               (workspace-id, action-id).
        :param str command_name: (optional) Schematics job command name.
        :param str command_parameter: (optional) Schematics job command parameter
               (playbook-name).
        :param List[str] command_options: (optional) Command line options for the
               command.
        :param List[VariableData] inputs: (optional) Job inputs used by Action or
               Workspace.
        :param List[VariableData] settings: (optional) Environment variables used
               by the Job while performing Action or Workspace.
        :param List[str] tags: (optional) User defined tags, while running the job.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param JobStatus status: (optional) Job Status.
        :param JobData data: (optional) Job data.
        :param BastionResourceDefinition bastion: (optional) Describes a bastion
               resource.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        """
        self.command_object = command_object
        self.command_object_id = command_object_id
        self.command_name = command_name
        self.command_parameter = command_parameter
        self.command_options = command_options
        self.inputs = inputs
        self.settings = settings
        self.tags = tags
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.resource_group = resource_group
        self.submitted_at = submitted_at
        self.submitted_by = submitted_by
        self.start_at = start_at
        self.end_at = end_at
        self.duration = duration
        self.status = status
        self.data = data
        self.bastion = bastion
        self.log_summary = log_summary
        self.log_store_url = log_store_url
        self.state_store_url = state_store_url
        self.results_url = results_url
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Job':
        """Initialize a Job object from a json dictionary."""
        args = {}
        if 'command_object' in _dict:
            args['command_object'] = _dict.get('command_object')
        if 'command_object_id' in _dict:
            args['command_object_id'] = _dict.get('command_object_id')
        if 'command_name' in _dict:
            args['command_name'] = _dict.get('command_name')
        if 'command_parameter' in _dict:
            args['command_parameter'] = _dict.get('command_parameter')
        if 'command_options' in _dict:
            args['command_options'] = _dict.get('command_options')
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'submitted_at' in _dict:
            args['submitted_at'] = string_to_datetime(_dict.get('submitted_at'))
        if 'submitted_by' in _dict:
            args['submitted_by'] = _dict.get('submitted_by')
        if 'start_at' in _dict:
            args['start_at'] = string_to_datetime(_dict.get('start_at'))
        if 'end_at' in _dict:
            args['end_at'] = string_to_datetime(_dict.get('end_at'))
        if 'duration' in _dict:
            args['duration'] = _dict.get('duration')
        if 'status' in _dict:
            args['status'] = JobStatus.from_dict(_dict.get('status'))
        if 'data' in _dict:
            args['data'] = JobData.from_dict(_dict.get('data'))
        if 'bastion' in _dict:
            args['bastion'] = BastionResourceDefinition.from_dict(_dict.get('bastion'))
        if 'log_summary' in _dict:
            args['log_summary'] = JobLogSummary.from_dict(_dict.get('log_summary'))
        if 'log_store_url' in _dict:
            args['log_store_url'] = _dict.get('log_store_url')
        if 'state_store_url' in _dict:
            args['state_store_url'] = _dict.get('state_store_url')
        if 'results_url' in _dict:
            args['results_url'] = _dict.get('results_url')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Job object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'command_object') and self.command_object is not None:
            _dict['command_object'] = self.command_object
        if hasattr(self, 'command_object_id') and self.command_object_id is not None:
            _dict['command_object_id'] = self.command_object_id
        if hasattr(self, 'command_name') and self.command_name is not None:
            _dict['command_name'] = self.command_name
        if hasattr(self, 'command_parameter') and self.command_parameter is not None:
            _dict['command_parameter'] = self.command_parameter
        if hasattr(self, 'command_options') and self.command_options is not None:
            _dict['command_options'] = self.command_options
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'name') and getattr(self, 'name') is not None:
            _dict['name'] = getattr(self, 'name')
        if hasattr(self, 'description') and getattr(self, 'description') is not None:
            _dict['description'] = getattr(self, 'description')
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and getattr(self, 'resource_group') is not None:
            _dict['resource_group'] = getattr(self, 'resource_group')
        if hasattr(self, 'submitted_at') and getattr(self, 'submitted_at') is not None:
            _dict['submitted_at'] = datetime_to_string(getattr(self, 'submitted_at'))
        if hasattr(self, 'submitted_by') and getattr(self, 'submitted_by') is not None:
            _dict['submitted_by'] = getattr(self, 'submitted_by')
        if hasattr(self, 'start_at') and getattr(self, 'start_at') is not None:
            _dict['start_at'] = datetime_to_string(getattr(self, 'start_at'))
        if hasattr(self, 'end_at') and getattr(self, 'end_at') is not None:
            _dict['end_at'] = datetime_to_string(getattr(self, 'end_at'))
        if hasattr(self, 'duration') and getattr(self, 'duration') is not None:
            _dict['duration'] = getattr(self, 'duration')
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status.to_dict()
        if hasattr(self, 'data') and self.data is not None:
            _dict['data'] = self.data.to_dict()
        if hasattr(self, 'bastion') and self.bastion is not None:
            _dict['bastion'] = self.bastion.to_dict()
        if hasattr(self, 'log_summary') and self.log_summary is not None:
            _dict['log_summary'] = self.log_summary.to_dict()
        if hasattr(self, 'log_store_url') and getattr(self, 'log_store_url') is not None:
            _dict['log_store_url'] = getattr(self, 'log_store_url')
        if hasattr(self, 'state_store_url') and getattr(self, 'state_store_url') is not None:
            _dict['state_store_url'] = getattr(self, 'state_store_url')
        if hasattr(self, 'results_url') and getattr(self, 'results_url') is not None:
            _dict['results_url'] = getattr(self, 'results_url')
        if hasattr(self, 'updated_at') and getattr(self, 'updated_at') is not None:
            _dict['updated_at'] = datetime_to_string(getattr(self, 'updated_at'))
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Job object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Job') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Job') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class CommandObjectEnum(str, Enum):
        """
        Name of the Schematics automation resource.
        """
        WORKSPACE = 'workspace'
        ACTION = 'action'
        SYSTEM = 'system'
        ENVIRONMENT = 'environment'


    class CommandNameEnum(str, Enum):
        """
        Schematics job command name.
        """
        WORKSPACE_PLAN = 'workspace_plan'
        WORKSPACE_APPLY = 'workspace_apply'
        WORKSPACE_DESTROY = 'workspace_destroy'
        WORKSPACE_REFRESH = 'workspace_refresh'
        ANSIBLE_PLAYBOOK_RUN = 'ansible_playbook_run'
        ANSIBLE_PLAYBOOK_CHECK = 'ansible_playbook_check'
        CREATE_ACTION = 'create_action'
        PUT_ACTION = 'put_action'
        PATCH_ACTION = 'patch_action'
        DELETE_ACTION = 'delete_action'
        SYSTEM_KEY_ENABLE = 'system_key_enable'
        SYSTEM_KEY_DELETE = 'system_key_delete'
        SYSTEM_KEY_DISABLE = 'system_key_disable'
        SYSTEM_KEY_ROTATE = 'system_key_rotate'
        SYSTEM_KEY_RESTORE = 'system_key_restore'
        CREATE_WORKSPACE = 'create_workspace'
        PUT_WORKSPACE = 'put_workspace'
        PATCH_WORKSPACE = 'patch_workspace'
        DELETE_WORKSPACE = 'delete_workspace'
        CREATE_CART = 'create_cart'
        CREATE_ENVIRONMENT = 'create_environment'
        PUT_ENVIRONMENT = 'put_environment'
        DELETE_ENVIRONMENT = 'delete_environment'
        ENVIRONMENT_INIT = 'environment_init'
        ENVIRONMENT_INSTALL = 'environment_install'
        ENVIRONMENT_UNINSTALL = 'environment_uninstall'
        REPOSITORY_PROCESS = 'repository_process'


    class LocationEnum(str, Enum):
        """
        List of locations supported by IBM Cloud Schematics service.  While creating your
        workspace or action, choose the right region, since it cannot be changed.  Note,
        this does not limit the location of the IBM Cloud resources, provisioned using
        Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


class JobData():
    """
    Job data.

    :attr str job_type: Type of Job.
    :attr JobDataWorkspace workspace_job_data: (optional) Workspace Job data.
    :attr JobDataAction action_job_data: (optional) Action Job data.
    :attr JobDataSystem system_job_data: (optional) Controls Job data.
    :attr JobDataFlow flow_job_data: (optional) Flow Job data.
    """

    def __init__(self,
                 job_type: str,
                 *,
                 workspace_job_data: 'JobDataWorkspace' = None,
                 action_job_data: 'JobDataAction' = None,
                 system_job_data: 'JobDataSystem' = None,
                 flow_job_data: 'JobDataFlow' = None) -> None:
        """
        Initialize a JobData object.

        :param str job_type: Type of Job.
        :param JobDataWorkspace workspace_job_data: (optional) Workspace Job data.
        :param JobDataAction action_job_data: (optional) Action Job data.
        :param JobDataSystem system_job_data: (optional) Controls Job data.
        :param JobDataFlow flow_job_data: (optional) Flow Job data.
        """
        self.job_type = job_type
        self.workspace_job_data = workspace_job_data
        self.action_job_data = action_job_data
        self.system_job_data = system_job_data
        self.flow_job_data = flow_job_data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobData':
        """Initialize a JobData object from a json dictionary."""
        args = {}
        if 'job_type' in _dict:
            args['job_type'] = _dict.get('job_type')
        else:
            raise ValueError('Required property \'job_type\' not present in JobData JSON')
        if 'workspace_job_data' in _dict:
            args['workspace_job_data'] = JobDataWorkspace.from_dict(_dict.get('workspace_job_data'))
        if 'action_job_data' in _dict:
            args['action_job_data'] = JobDataAction.from_dict(_dict.get('action_job_data'))
        if 'system_job_data' in _dict:
            args['system_job_data'] = JobDataSystem.from_dict(_dict.get('system_job_data'))
        if 'flow_job_data' in _dict:
            args['flow_job_data'] = JobDataFlow.from_dict(_dict.get('flow_job_data'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job_type') and self.job_type is not None:
            _dict['job_type'] = self.job_type
        if hasattr(self, 'workspace_job_data') and self.workspace_job_data is not None:
            _dict['workspace_job_data'] = self.workspace_job_data.to_dict()
        if hasattr(self, 'action_job_data') and self.action_job_data is not None:
            _dict['action_job_data'] = self.action_job_data.to_dict()
        if hasattr(self, 'system_job_data') and self.system_job_data is not None:
            _dict['system_job_data'] = self.system_job_data.to_dict()
        if hasattr(self, 'flow_job_data') and self.flow_job_data is not None:
            _dict['flow_job_data'] = self.flow_job_data.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class JobTypeEnum(str, Enum):
        """
        Type of Job.
        """
        REPO_DOWNLOAD_JOB = 'repo_download_job'
        WORKSPACE_JOB = 'workspace_job'
        ACTION_JOB = 'action_job'
        SYSTEM_JOB = 'system_job'
        FLOW_JOB = 'flow-job'


class JobDataAction():
    """
    Action Job data.

    :attr str action_name: (optional) Flow name.
    :attr List[VariableData] inputs: (optional) Input variables data used by the
          Action Job.
    :attr List[VariableData] outputs: (optional) Output variables data from the
          Action Job.
    :attr List[VariableData] settings: (optional) Environment variables used by all
          the templates in the Action.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    :attr InventoryResourceRecord inventory_record: (optional) Complete inventory
          resource details with user inputs and system generated data.
    :attr str materialized_inventory: (optional) Materialized inventory details used
          by the Action Job, in .ini format.
    """

    def __init__(self,
                 *,
                 action_name: str = None,
                 inputs: List['VariableData'] = None,
                 outputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 updated_at: datetime = None,
                 inventory_record: 'InventoryResourceRecord' = None,
                 materialized_inventory: str = None) -> None:
        """
        Initialize a JobDataAction object.

        :param str action_name: (optional) Flow name.
        :param List[VariableData] inputs: (optional) Input variables data used by
               the Action Job.
        :param List[VariableData] outputs: (optional) Output variables data from
               the Action Job.
        :param List[VariableData] settings: (optional) Environment variables used
               by all the templates in the Action.
        :param datetime updated_at: (optional) Job status updation timestamp.
        :param InventoryResourceRecord inventory_record: (optional) Complete
               inventory resource details with user inputs and system generated data.
        :param str materialized_inventory: (optional) Materialized inventory
               details used by the Action Job, in .ini format.
        """
        self.action_name = action_name
        self.inputs = inputs
        self.outputs = outputs
        self.settings = settings
        self.updated_at = updated_at
        self.inventory_record = inventory_record
        self.materialized_inventory = materialized_inventory

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataAction':
        """Initialize a JobDataAction object from a json dictionary."""
        args = {}
        if 'action_name' in _dict:
            args['action_name'] = _dict.get('action_name')
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'outputs' in _dict:
            args['outputs'] = [VariableData.from_dict(x) for x in _dict.get('outputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'inventory_record' in _dict:
            args['inventory_record'] = InventoryResourceRecord.from_dict(_dict.get('inventory_record'))
        if 'materialized_inventory' in _dict:
            args['materialized_inventory'] = _dict.get('materialized_inventory')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataAction object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_name') and self.action_name is not None:
            _dict['action_name'] = self.action_name
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'outputs') and self.outputs is not None:
            _dict['outputs'] = [x.to_dict() for x in self.outputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        if hasattr(self, 'inventory_record') and self.inventory_record is not None:
            _dict['inventory_record'] = self.inventory_record.to_dict()
        if hasattr(self, 'materialized_inventory') and self.materialized_inventory is not None:
            _dict['materialized_inventory'] = self.materialized_inventory
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataAction object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataAction') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataAction') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobDataFlow():
    """
    Flow Job data.

    :attr str flow_id: (optional) Flow ID.
    :attr str flow_name: (optional) Flow Name.
    :attr List[JobDataWorkItem] workitems: (optional) Job data used by each workitem
          Job.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 flow_id: str = None,
                 flow_name: str = None,
                 workitems: List['JobDataWorkItem'] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobDataFlow object.

        :param str flow_id: (optional) Flow ID.
        :param str flow_name: (optional) Flow Name.
        :param List[JobDataWorkItem] workitems: (optional) Job data used by each
               workitem Job.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.flow_id = flow_id
        self.flow_name = flow_name
        self.workitems = workitems
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataFlow':
        """Initialize a JobDataFlow object from a json dictionary."""
        args = {}
        if 'flow_id' in _dict:
            args['flow_id'] = _dict.get('flow_id')
        if 'flow_name' in _dict:
            args['flow_name'] = _dict.get('flow_name')
        if 'workitems' in _dict:
            args['workitems'] = [JobDataWorkItem.from_dict(x) for x in _dict.get('workitems')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataFlow object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'flow_id') and self.flow_id is not None:
            _dict['flow_id'] = self.flow_id
        if hasattr(self, 'flow_name') and self.flow_name is not None:
            _dict['flow_name'] = self.flow_name
        if hasattr(self, 'workitems') and self.workitems is not None:
            _dict['workitems'] = [x.to_dict() for x in self.workitems]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataFlow object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataFlow') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataFlow') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobDataSystem():
    """
    Controls Job data.

    :attr str key_id: (optional) Key ID for which key event is generated.
    :attr List[str] schematics_resource_id: (optional) List of the schematics
          resource id.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 key_id: str = None,
                 schematics_resource_id: List[str] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobDataSystem object.

        :param str key_id: (optional) Key ID for which key event is generated.
        :param List[str] schematics_resource_id: (optional) List of the schematics
               resource id.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.key_id = key_id
        self.schematics_resource_id = schematics_resource_id
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataSystem':
        """Initialize a JobDataSystem object from a json dictionary."""
        args = {}
        if 'key_id' in _dict:
            args['key_id'] = _dict.get('key_id')
        if 'schematics_resource_id' in _dict:
            args['schematics_resource_id'] = _dict.get('schematics_resource_id')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataSystem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'key_id') and self.key_id is not None:
            _dict['key_id'] = self.key_id
        if hasattr(self, 'schematics_resource_id') and self.schematics_resource_id is not None:
            _dict['schematics_resource_id'] = self.schematics_resource_id
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataSystem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataSystem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataSystem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobDataTemplate():
    """
    Template Job data.

    :attr str template_id: (optional) Template Id.
    :attr str template_name: (optional) Template name.
    :attr int flow_index: (optional) Index of the template in the Flow.
    :attr List[VariableData] inputs: (optional) Job inputs used by the Templates.
    :attr List[VariableData] outputs: (optional) Job output from the Templates.
    :attr List[VariableData] settings: (optional) Environment variables used by the
          template.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 template_id: str = None,
                 template_name: str = None,
                 flow_index: int = None,
                 inputs: List['VariableData'] = None,
                 outputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobDataTemplate object.

        :param str template_id: (optional) Template Id.
        :param str template_name: (optional) Template name.
        :param int flow_index: (optional) Index of the template in the Flow.
        :param List[VariableData] inputs: (optional) Job inputs used by the
               Templates.
        :param List[VariableData] outputs: (optional) Job output from the
               Templates.
        :param List[VariableData] settings: (optional) Environment variables used
               by the template.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.template_id = template_id
        self.template_name = template_name
        self.flow_index = flow_index
        self.inputs = inputs
        self.outputs = outputs
        self.settings = settings
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataTemplate':
        """Initialize a JobDataTemplate object from a json dictionary."""
        args = {}
        if 'template_id' in _dict:
            args['template_id'] = _dict.get('template_id')
        if 'template_name' in _dict:
            args['template_name'] = _dict.get('template_name')
        if 'flow_index' in _dict:
            args['flow_index'] = _dict.get('flow_index')
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'outputs' in _dict:
            args['outputs'] = [VariableData.from_dict(x) for x in _dict.get('outputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataTemplate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'template_id') and self.template_id is not None:
            _dict['template_id'] = self.template_id
        if hasattr(self, 'template_name') and self.template_name is not None:
            _dict['template_name'] = self.template_name
        if hasattr(self, 'flow_index') and self.flow_index is not None:
            _dict['flow_index'] = self.flow_index
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'outputs') and self.outputs is not None:
            _dict['outputs'] = [x.to_dict() for x in self.outputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataTemplate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataTemplate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataTemplate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobDataWorkItem():
    """
    Environment work items.

    :attr str command_object_id: (optional) command object id.
    :attr str command_object_name: (optional) command object name.
    :attr str layers: (optional) layer name.
    :attr str source_type: (optional) Type of source for the Template.
    :attr ExternalSource source: (optional) Source of templates, playbooks, or
          controls.
    :attr List[VariableData] inputs: (optional) Input variables data for the
          workItem used in FlowJob.
    :attr List[VariableData] outputs: (optional) Output variables for the workItem.
    :attr List[VariableData] settings: (optional) Environment variables for the
          workItem.
    :attr JobDataWorkItemLastJob last_job: (optional) Status of the last job
          executed by the workitem.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 command_object_id: str = None,
                 command_object_name: str = None,
                 layers: str = None,
                 source_type: str = None,
                 source: 'ExternalSource' = None,
                 inputs: List['VariableData'] = None,
                 outputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 last_job: 'JobDataWorkItemLastJob' = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobDataWorkItem object.

        :param str command_object_id: (optional) command object id.
        :param str command_object_name: (optional) command object name.
        :param str layers: (optional) layer name.
        :param str source_type: (optional) Type of source for the Template.
        :param ExternalSource source: (optional) Source of templates, playbooks, or
               controls.
        :param List[VariableData] inputs: (optional) Input variables data for the
               workItem used in FlowJob.
        :param List[VariableData] outputs: (optional) Output variables for the
               workItem.
        :param List[VariableData] settings: (optional) Environment variables for
               the workItem.
        :param JobDataWorkItemLastJob last_job: (optional) Status of the last job
               executed by the workitem.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.command_object_id = command_object_id
        self.command_object_name = command_object_name
        self.layers = layers
        self.source_type = source_type
        self.source = source
        self.inputs = inputs
        self.outputs = outputs
        self.settings = settings
        self.last_job = last_job
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataWorkItem':
        """Initialize a JobDataWorkItem object from a json dictionary."""
        args = {}
        if 'command_object_id' in _dict:
            args['command_object_id'] = _dict.get('command_object_id')
        if 'command_object_name' in _dict:
            args['command_object_name'] = _dict.get('command_object_name')
        if 'layers' in _dict:
            args['layers'] = _dict.get('layers')
        if 'source_type' in _dict:
            args['source_type'] = _dict.get('source_type')
        if 'source' in _dict:
            args['source'] = ExternalSource.from_dict(_dict.get('source'))
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'outputs' in _dict:
            args['outputs'] = [VariableData.from_dict(x) for x in _dict.get('outputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'last_job' in _dict:
            args['last_job'] = JobDataWorkItemLastJob.from_dict(_dict.get('last_job'))
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataWorkItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'command_object_id') and self.command_object_id is not None:
            _dict['command_object_id'] = self.command_object_id
        if hasattr(self, 'command_object_name') and self.command_object_name is not None:
            _dict['command_object_name'] = self.command_object_name
        if hasattr(self, 'layers') and self.layers is not None:
            _dict['layers'] = self.layers
        if hasattr(self, 'source_type') and self.source_type is not None:
            _dict['source_type'] = self.source_type
        if hasattr(self, 'source') and self.source is not None:
            _dict['source'] = self.source.to_dict()
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'outputs') and self.outputs is not None:
            _dict['outputs'] = [x.to_dict() for x in self.outputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'last_job') and self.last_job is not None:
            _dict['last_job'] = self.last_job.to_dict()
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataWorkItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataWorkItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataWorkItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class SourceTypeEnum(str, Enum):
        """
        Type of source for the Template.
        """
        LOCAL = 'local'
        GIT_HUB = 'git_hub'
        GIT_HUB_ENTERPRISE = 'git_hub_enterprise'
        GIT_LAB = 'git_lab'
        IBM_GIT_LAB = 'ibm_git_lab'
        IBM_CLOUD_CATALOG = 'ibm_cloud_catalog'
        EXTERNAL_SCM = 'external_scm'
        COS_BUCKET = 'cos_bucket'


class JobDataWorkItemLastJob():
    """
    Status of the last job executed by the workitem.

    :attr str command_object: (optional) Name of the Schematics automation resource.
    :attr str command_object_name: (optional) command object name
          (workspace_name/action_name).
    :attr str command_object_id: (optional) Workitem command object id, maps to
          workspace_id or action_id.
    :attr str command_name: (optional) Schematics job command name.
    :attr str job_id: (optional) Workspace job id.
    :attr str job_status: (optional) Status of Jobs.
    """

    def __init__(self,
                 *,
                 command_object: str = None,
                 command_object_name: str = None,
                 command_object_id: str = None,
                 command_name: str = None,
                 job_id: str = None,
                 job_status: str = None) -> None:
        """
        Initialize a JobDataWorkItemLastJob object.

        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_name: (optional) command object name
               (workspace_name/action_name).
        :param str command_object_id: (optional) Workitem command object id, maps
               to workspace_id or action_id.
        :param str command_name: (optional) Schematics job command name.
        :param str job_id: (optional) Workspace job id.
        :param str job_status: (optional) Status of Jobs.
        """
        self.command_object = command_object
        self.command_object_name = command_object_name
        self.command_object_id = command_object_id
        self.command_name = command_name
        self.job_id = job_id
        self.job_status = job_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataWorkItemLastJob':
        """Initialize a JobDataWorkItemLastJob object from a json dictionary."""
        args = {}
        if 'command_object' in _dict:
            args['command_object'] = _dict.get('command_object')
        if 'command_object_name' in _dict:
            args['command_object_name'] = _dict.get('command_object_name')
        if 'command_object_id' in _dict:
            args['command_object_id'] = _dict.get('command_object_id')
        if 'command_name' in _dict:
            args['command_name'] = _dict.get('command_name')
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        if 'job_status' in _dict:
            args['job_status'] = _dict.get('job_status')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataWorkItemLastJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'command_object') and self.command_object is not None:
            _dict['command_object'] = self.command_object
        if hasattr(self, 'command_object_name') and self.command_object_name is not None:
            _dict['command_object_name'] = self.command_object_name
        if hasattr(self, 'command_object_id') and self.command_object_id is not None:
            _dict['command_object_id'] = self.command_object_id
        if hasattr(self, 'command_name') and self.command_name is not None:
            _dict['command_name'] = self.command_name
        if hasattr(self, 'job_id') and self.job_id is not None:
            _dict['job_id'] = self.job_id
        if hasattr(self, 'job_status') and self.job_status is not None:
            _dict['job_status'] = self.job_status
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataWorkItemLastJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataWorkItemLastJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataWorkItemLastJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class CommandObjectEnum(str, Enum):
        """
        Name of the Schematics automation resource.
        """
        WORKSPACE = 'workspace'
        ACTION = 'action'
        SYSTEM = 'system'
        ENVIRONMENT = 'environment'


    class CommandNameEnum(str, Enum):
        """
        Schematics job command name.
        """
        WORKSPACE_PLAN = 'workspace_plan'
        WORKSPACE_APPLY = 'workspace_apply'
        WORKSPACE_DESTROY = 'workspace_destroy'
        WORKSPACE_REFRESH = 'workspace_refresh'
        ANSIBLE_PLAYBOOK_RUN = 'ansible_playbook_run'
        ANSIBLE_PLAYBOOK_CHECK = 'ansible_playbook_check'
        CREATE_ACTION = 'create_action'
        PUT_ACTION = 'put_action'
        PATCH_ACTION = 'patch_action'
        DELETE_ACTION = 'delete_action'
        SYSTEM_KEY_ENABLE = 'system_key_enable'
        SYSTEM_KEY_DELETE = 'system_key_delete'
        SYSTEM_KEY_DISABLE = 'system_key_disable'
        SYSTEM_KEY_ROTATE = 'system_key_rotate'
        SYSTEM_KEY_RESTORE = 'system_key_restore'
        CREATE_WORKSPACE = 'create_workspace'
        PUT_WORKSPACE = 'put_workspace'
        PATCH_WORKSPACE = 'patch_workspace'
        DELETE_WORKSPACE = 'delete_workspace'
        CREATE_CART = 'create_cart'
        CREATE_ENVIRONMENT = 'create_environment'
        PUT_ENVIRONMENT = 'put_environment'
        DELETE_ENVIRONMENT = 'delete_environment'
        ENVIRONMENT_INIT = 'environment_init'
        ENVIRONMENT_INSTALL = 'environment_install'
        ENVIRONMENT_UNINSTALL = 'environment_uninstall'
        REPOSITORY_PROCESS = 'repository_process'


    class JobStatusEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        JOB_FINISHED = 'job_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class JobDataWorkspace():
    """
    Workspace Job data.

    :attr str workspace_name: (optional) Workspace name.
    :attr str flow_id: (optional) Flow Id.
    :attr str flow_name: (optional) Flow name.
    :attr List[VariableData] inputs: (optional) Input variables data used by the
          Workspace Job.
    :attr List[VariableData] outputs: (optional) Output variables data from the
          Workspace Job.
    :attr List[VariableData] settings: (optional) Environment variables used by all
          the templates in the Workspace.
    :attr List[JobDataTemplate] template_data: (optional) Input / output data of the
          Template in the Workspace Job.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 workspace_name: str = None,
                 flow_id: str = None,
                 flow_name: str = None,
                 inputs: List['VariableData'] = None,
                 outputs: List['VariableData'] = None,
                 settings: List['VariableData'] = None,
                 template_data: List['JobDataTemplate'] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobDataWorkspace object.

        :param str workspace_name: (optional) Workspace name.
        :param str flow_id: (optional) Flow Id.
        :param str flow_name: (optional) Flow name.
        :param List[VariableData] inputs: (optional) Input variables data used by
               the Workspace Job.
        :param List[VariableData] outputs: (optional) Output variables data from
               the Workspace Job.
        :param List[VariableData] settings: (optional) Environment variables used
               by all the templates in the Workspace.
        :param List[JobDataTemplate] template_data: (optional) Input / output data
               of the Template in the Workspace Job.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.workspace_name = workspace_name
        self.flow_id = flow_id
        self.flow_name = flow_name
        self.inputs = inputs
        self.outputs = outputs
        self.settings = settings
        self.template_data = template_data
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobDataWorkspace':
        """Initialize a JobDataWorkspace object from a json dictionary."""
        args = {}
        if 'workspace_name' in _dict:
            args['workspace_name'] = _dict.get('workspace_name')
        if 'flow_id' in _dict:
            args['flow_id'] = _dict.get('flow_id')
        if 'flow_name' in _dict:
            args['flow_name'] = _dict.get('flow_name')
        if 'inputs' in _dict:
            args['inputs'] = [VariableData.from_dict(x) for x in _dict.get('inputs')]
        if 'outputs' in _dict:
            args['outputs'] = [VariableData.from_dict(x) for x in _dict.get('outputs')]
        if 'settings' in _dict:
            args['settings'] = [VariableData.from_dict(x) for x in _dict.get('settings')]
        if 'template_data' in _dict:
            args['template_data'] = [JobDataTemplate.from_dict(x) for x in _dict.get('template_data')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobDataWorkspace object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'workspace_name') and self.workspace_name is not None:
            _dict['workspace_name'] = self.workspace_name
        if hasattr(self, 'flow_id') and self.flow_id is not None:
            _dict['flow_id'] = self.flow_id
        if hasattr(self, 'flow_name') and self.flow_name is not None:
            _dict['flow_name'] = self.flow_name
        if hasattr(self, 'inputs') and self.inputs is not None:
            _dict['inputs'] = [x.to_dict() for x in self.inputs]
        if hasattr(self, 'outputs') and self.outputs is not None:
            _dict['outputs'] = [x.to_dict() for x in self.outputs]
        if hasattr(self, 'settings') and self.settings is not None:
            _dict['settings'] = [x.to_dict() for x in self.settings]
        if hasattr(self, 'template_data') and self.template_data is not None:
            _dict['template_data'] = [x.to_dict() for x in self.template_data]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobDataWorkspace object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobDataWorkspace') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobDataWorkspace') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobList():
    """
    List of Job details.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[JobLite] jobs: (optional) List of job records.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 jobs: List['JobLite'] = None) -> None:
        """
        Initialize a JobList object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[JobLite] jobs: (optional) List of job records.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.jobs = jobs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobList':
        """Initialize a JobList object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in JobList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in JobList JSON')
        if 'jobs' in _dict:
            args['jobs'] = [JobLite.from_dict(x) for x in _dict.get('jobs')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'jobs') and self.jobs is not None:
            _dict['jobs'] = [x.to_dict() for x in self.jobs]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLite():
    """
    Job summary profile with system generated data.

    :attr str id: (optional) Job ID.
    :attr str name: (optional) Job name, uniquely derived from the related Workspace
          or Action.
    :attr str description: (optional) Job description derived from the related
          Workspace or Action.
    :attr str command_object: (optional) Name of the Schematics automation resource.
    :attr str command_object_id: (optional) Job command object id (workspace-id,
          action-id).
    :attr str command_name: (optional) Schematics job command name.
    :attr List[str] tags: (optional) User defined tags, while running the job.
    :attr str location: (optional) List of locations supported by IBM Cloud
          Schematics service.  While creating your workspace or action, choose the right
          region, since it cannot be changed.  Note, this does not limit the location of
          the IBM Cloud resources, provisioned using Schematics.
    :attr str resource_group: (optional) Resource-group name derived from the
          related Workspace or Action.
    :attr datetime submitted_at: (optional) Job submission time.
    :attr str submitted_by: (optional) Email address of user who submitted the job.
    :attr str duration: (optional) Duration of job execution; example 40 sec.
    :attr datetime start_at: (optional) Job start time.
    :attr datetime end_at: (optional) Job end time.
    :attr JobStatus status: (optional) Job Status.
    :attr JobLogSummary log_summary: (optional) Job log summary record.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 command_object: str = None,
                 command_object_id: str = None,
                 command_name: str = None,
                 tags: List[str] = None,
                 location: str = None,
                 resource_group: str = None,
                 submitted_at: datetime = None,
                 submitted_by: str = None,
                 duration: str = None,
                 start_at: datetime = None,
                 end_at: datetime = None,
                 status: 'JobStatus' = None,
                 log_summary: 'JobLogSummary' = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobLite object.

        :param str id: (optional) Job ID.
        :param str name: (optional) Job name, uniquely derived from the related
               Workspace or Action.
        :param str description: (optional) Job description derived from the related
               Workspace or Action.
        :param str command_object: (optional) Name of the Schematics automation
               resource.
        :param str command_object_id: (optional) Job command object id
               (workspace-id, action-id).
        :param str command_name: (optional) Schematics job command name.
        :param List[str] tags: (optional) User defined tags, while running the job.
        :param str location: (optional) List of locations supported by IBM Cloud
               Schematics service.  While creating your workspace or action, choose the
               right region, since it cannot be changed.  Note, this does not limit the
               location of the IBM Cloud resources, provisioned using Schematics.
        :param str resource_group: (optional) Resource-group name derived from the
               related Workspace or Action.
        :param datetime submitted_at: (optional) Job submission time.
        :param str submitted_by: (optional) Email address of user who submitted the
               job.
        :param str duration: (optional) Duration of job execution; example 40 sec.
        :param datetime start_at: (optional) Job start time.
        :param datetime end_at: (optional) Job end time.
        :param JobStatus status: (optional) Job Status.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.id = id
        self.name = name
        self.description = description
        self.command_object = command_object
        self.command_object_id = command_object_id
        self.command_name = command_name
        self.tags = tags
        self.location = location
        self.resource_group = resource_group
        self.submitted_at = submitted_at
        self.submitted_by = submitted_by
        self.duration = duration
        self.start_at = start_at
        self.end_at = end_at
        self.status = status
        self.log_summary = log_summary
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLite':
        """Initialize a JobLite object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'command_object' in _dict:
            args['command_object'] = _dict.get('command_object')
        if 'command_object_id' in _dict:
            args['command_object_id'] = _dict.get('command_object_id')
        if 'command_name' in _dict:
            args['command_name'] = _dict.get('command_name')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'submitted_at' in _dict:
            args['submitted_at'] = string_to_datetime(_dict.get('submitted_at'))
        if 'submitted_by' in _dict:
            args['submitted_by'] = _dict.get('submitted_by')
        if 'duration' in _dict:
            args['duration'] = _dict.get('duration')
        if 'start_at' in _dict:
            args['start_at'] = string_to_datetime(_dict.get('start_at'))
        if 'end_at' in _dict:
            args['end_at'] = string_to_datetime(_dict.get('end_at'))
        if 'status' in _dict:
            args['status'] = JobStatus.from_dict(_dict.get('status'))
        if 'log_summary' in _dict:
            args['log_summary'] = JobLogSummary.from_dict(_dict.get('log_summary'))
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLite object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'command_object') and self.command_object is not None:
            _dict['command_object'] = self.command_object
        if hasattr(self, 'command_object_id') and self.command_object_id is not None:
            _dict['command_object_id'] = self.command_object_id
        if hasattr(self, 'command_name') and self.command_name is not None:
            _dict['command_name'] = self.command_name
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'submitted_at') and self.submitted_at is not None:
            _dict['submitted_at'] = datetime_to_string(self.submitted_at)
        if hasattr(self, 'submitted_by') and self.submitted_by is not None:
            _dict['submitted_by'] = self.submitted_by
        if hasattr(self, 'duration') and self.duration is not None:
            _dict['duration'] = self.duration
        if hasattr(self, 'start_at') and self.start_at is not None:
            _dict['start_at'] = datetime_to_string(self.start_at)
        if hasattr(self, 'end_at') and self.end_at is not None:
            _dict['end_at'] = datetime_to_string(self.end_at)
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status.to_dict()
        if hasattr(self, 'log_summary') and self.log_summary is not None:
            _dict['log_summary'] = self.log_summary.to_dict()
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLite object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLite') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLite') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class CommandObjectEnum(str, Enum):
        """
        Name of the Schematics automation resource.
        """
        WORKSPACE = 'workspace'
        ACTION = 'action'
        SYSTEM = 'system'
        ENVIRONMENT = 'environment'


    class CommandNameEnum(str, Enum):
        """
        Schematics job command name.
        """
        WORKSPACE_PLAN = 'workspace_plan'
        WORKSPACE_APPLY = 'workspace_apply'
        WORKSPACE_DESTROY = 'workspace_destroy'
        WORKSPACE_REFRESH = 'workspace_refresh'
        ANSIBLE_PLAYBOOK_RUN = 'ansible_playbook_run'
        ANSIBLE_PLAYBOOK_CHECK = 'ansible_playbook_check'
        CREATE_ACTION = 'create_action'
        PUT_ACTION = 'put_action'
        PATCH_ACTION = 'patch_action'
        DELETE_ACTION = 'delete_action'
        SYSTEM_KEY_ENABLE = 'system_key_enable'
        SYSTEM_KEY_DELETE = 'system_key_delete'
        SYSTEM_KEY_DISABLE = 'system_key_disable'
        SYSTEM_KEY_ROTATE = 'system_key_rotate'
        SYSTEM_KEY_RESTORE = 'system_key_restore'
        CREATE_WORKSPACE = 'create_workspace'
        PUT_WORKSPACE = 'put_workspace'
        PATCH_WORKSPACE = 'patch_workspace'
        DELETE_WORKSPACE = 'delete_workspace'
        CREATE_CART = 'create_cart'
        CREATE_ENVIRONMENT = 'create_environment'
        PUT_ENVIRONMENT = 'put_environment'
        DELETE_ENVIRONMENT = 'delete_environment'
        ENVIRONMENT_INIT = 'environment_init'
        ENVIRONMENT_INSTALL = 'environment_install'
        ENVIRONMENT_UNINSTALL = 'environment_uninstall'
        REPOSITORY_PROCESS = 'repository_process'


    class LocationEnum(str, Enum):
        """
        List of locations supported by IBM Cloud Schematics service.  While creating your
        workspace or action, choose the right region, since it cannot be changed.  Note,
        this does not limit the location of the IBM Cloud resources, provisioned using
        Schematics.
        """
        US_SOUTH = 'us-south'
        US_EAST = 'us-east'
        EU_GB = 'eu-gb'
        EU_DE = 'eu-de'


class JobLog():
    """
    Job Log details.

    :attr str job_id: (optional) Job Id.
    :attr str job_name: (optional) Job name, uniquely derived from the related
          Workspace, Action or Controls.
    :attr JobLogSummary log_summary: (optional) Job log summary record.
    :attr str format: (optional) Format of the Log text.
    :attr bytes details: (optional) Log text, generated by the Job.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 job_id: str = None,
                 job_name: str = None,
                 log_summary: 'JobLogSummary' = None,
                 format: str = None,
                 details: bytes = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobLog object.

        :param str job_id: (optional) Job Id.
        :param str job_name: (optional) Job name, uniquely derived from the related
               Workspace, Action or Controls.
        :param JobLogSummary log_summary: (optional) Job log summary record.
        :param str format: (optional) Format of the Log text.
        :param bytes details: (optional) Log text, generated by the Job.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.job_id = job_id
        self.job_name = job_name
        self.log_summary = log_summary
        self.format = format
        self.details = details
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLog':
        """Initialize a JobLog object from a json dictionary."""
        args = {}
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        if 'job_name' in _dict:
            args['job_name'] = _dict.get('job_name')
        if 'log_summary' in _dict:
            args['log_summary'] = JobLogSummary.from_dict(_dict.get('log_summary'))
        if 'format' in _dict:
            args['format'] = _dict.get('format')
        if 'details' in _dict:
            args['details'] = base64.b64decode(_dict.get('details'))
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLog object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job_id') and self.job_id is not None:
            _dict['job_id'] = self.job_id
        if hasattr(self, 'job_name') and self.job_name is not None:
            _dict['job_name'] = self.job_name
        if hasattr(self, 'log_summary') and self.log_summary is not None:
            _dict['log_summary'] = self.log_summary.to_dict()
        if hasattr(self, 'format') and self.format is not None:
            _dict['format'] = self.format
        if hasattr(self, 'details') and self.details is not None:
            _dict['details'] = str(base64.b64encode(self.details), 'utf-8')
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLog object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLog') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLog') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class FormatEnum(str, Enum):
        """
        Format of the Log text.
        """
        JSON = 'json'
        HTML = 'html'
        MARKDOWN = 'markdown'
        RTF = 'rtf'


class JobLogSummary():
    """
    Job log summary record.

    :attr str job_id: (optional) Workspace Id.
    :attr str job_type: (optional) Type of Job.
    :attr datetime log_start_at: (optional) Job log start timestamp.
    :attr datetime log_analyzed_till: (optional) Job log update timestamp.
    :attr float elapsed_time: (optional) Job log elapsed time (log_analyzed_till -
          log_start_at).
    :attr List[JobLogSummaryLogErrors] log_errors: (optional) Job log errors.
    :attr JobLogSummaryRepoDownloadJob repo_download_job: (optional) Repo download
          Job log summary.
    :attr JobLogSummaryWorkspaceJob workspace_job: (optional) Workspace Job log
          summary.
    :attr JobLogSummaryFlowJob flow_job: (optional) Flow Job log summary.
    :attr JobLogSummaryActionJob action_job: (optional) Flow Job log summary.
    :attr JobLogSummarySystemJob system_job: (optional) System Job log summary.
    """

    def __init__(self,
                 *,
                 job_id: str = None,
                 job_type: str = None,
                 log_start_at: datetime = None,
                 log_analyzed_till: datetime = None,
                 elapsed_time: float = None,
                 log_errors: List['JobLogSummaryLogErrors'] = None,
                 repo_download_job: 'JobLogSummaryRepoDownloadJob' = None,
                 workspace_job: 'JobLogSummaryWorkspaceJob' = None,
                 flow_job: 'JobLogSummaryFlowJob' = None,
                 action_job: 'JobLogSummaryActionJob' = None,
                 system_job: 'JobLogSummarySystemJob' = None) -> None:
        """
        Initialize a JobLogSummary object.

        :param str job_type: (optional) Type of Job.
        :param JobLogSummaryRepoDownloadJob repo_download_job: (optional) Repo
               download Job log summary.
        :param JobLogSummaryWorkspaceJob workspace_job: (optional) Workspace Job
               log summary.
        :param JobLogSummaryFlowJob flow_job: (optional) Flow Job log summary.
        :param JobLogSummaryActionJob action_job: (optional) Flow Job log summary.
        :param JobLogSummarySystemJob system_job: (optional) System Job log
               summary.
        """
        self.job_id = job_id
        self.job_type = job_type
        self.log_start_at = log_start_at
        self.log_analyzed_till = log_analyzed_till
        self.elapsed_time = elapsed_time
        self.log_errors = log_errors
        self.repo_download_job = repo_download_job
        self.workspace_job = workspace_job
        self.flow_job = flow_job
        self.action_job = action_job
        self.system_job = system_job

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummary':
        """Initialize a JobLogSummary object from a json dictionary."""
        args = {}
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        if 'job_type' in _dict:
            args['job_type'] = _dict.get('job_type')
        if 'log_start_at' in _dict:
            args['log_start_at'] = string_to_datetime(_dict.get('log_start_at'))
        if 'log_analyzed_till' in _dict:
            args['log_analyzed_till'] = string_to_datetime(_dict.get('log_analyzed_till'))
        if 'elapsed_time' in _dict:
            args['elapsed_time'] = _dict.get('elapsed_time')
        if 'log_errors' in _dict:
            args['log_errors'] = [JobLogSummaryLogErrors.from_dict(x) for x in _dict.get('log_errors')]
        if 'repo_download_job' in _dict:
            args['repo_download_job'] = JobLogSummaryRepoDownloadJob.from_dict(_dict.get('repo_download_job'))
        if 'workspace_job' in _dict:
            args['workspace_job'] = JobLogSummaryWorkspaceJob.from_dict(_dict.get('workspace_job'))
        if 'flow_job' in _dict:
            args['flow_job'] = JobLogSummaryFlowJob.from_dict(_dict.get('flow_job'))
        if 'action_job' in _dict:
            args['action_job'] = JobLogSummaryActionJob.from_dict(_dict.get('action_job'))
        if 'system_job' in _dict:
            args['system_job'] = JobLogSummarySystemJob.from_dict(_dict.get('system_job'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummary object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job_id') and getattr(self, 'job_id') is not None:
            _dict['job_id'] = getattr(self, 'job_id')
        if hasattr(self, 'job_type') and self.job_type is not None:
            _dict['job_type'] = self.job_type
        if hasattr(self, 'log_start_at') and getattr(self, 'log_start_at') is not None:
            _dict['log_start_at'] = datetime_to_string(getattr(self, 'log_start_at'))
        if hasattr(self, 'log_analyzed_till') and getattr(self, 'log_analyzed_till') is not None:
            _dict['log_analyzed_till'] = datetime_to_string(getattr(self, 'log_analyzed_till'))
        if hasattr(self, 'elapsed_time') and getattr(self, 'elapsed_time') is not None:
            _dict['elapsed_time'] = getattr(self, 'elapsed_time')
        if hasattr(self, 'log_errors') and getattr(self, 'log_errors') is not None:
            _dict['log_errors'] = [x.to_dict() for x in getattr(self, 'log_errors')]
        if hasattr(self, 'repo_download_job') and self.repo_download_job is not None:
            _dict['repo_download_job'] = self.repo_download_job.to_dict()
        if hasattr(self, 'workspace_job') and self.workspace_job is not None:
            _dict['workspace_job'] = self.workspace_job.to_dict()
        if hasattr(self, 'flow_job') and self.flow_job is not None:
            _dict['flow_job'] = self.flow_job.to_dict()
        if hasattr(self, 'action_job') and self.action_job is not None:
            _dict['action_job'] = self.action_job.to_dict()
        if hasattr(self, 'system_job') and self.system_job is not None:
            _dict['system_job'] = self.system_job.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummary object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummary') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummary') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class JobTypeEnum(str, Enum):
        """
        Type of Job.
        """
        REPO_DOWNLOAD_JOB = 'repo_download_job'
        WORKSPACE_JOB = 'workspace_job'
        ACTION_JOB = 'action_job'
        SYSTEM_JOB = 'system_job'
        FLOW_JOB = 'flow_job'


class JobLogSummaryWorkitems():
    """
    Job log summary of the flow workitem.

    :attr str workspace_id: (optional) workspace ID.
    :attr str job_id: (optional) workspace JOB ID.
    :attr float resources_add: (optional) Number of resources add.
    :attr float resources_modify: (optional) Number of resources modify.
    :attr float resources_destroy: (optional) Number of resources destroy.
    :attr str log_url: (optional) Log url for job.
    """

    def __init__(self,
                 *,
                 workspace_id: str = None,
                 job_id: str = None,
                 resources_add: float = None,
                 resources_modify: float = None,
                 resources_destroy: float = None,
                 log_url: str = None) -> None:
        """
        Initialize a JobLogSummaryWorkitems object.

        :param str workspace_id: (optional) workspace ID.
        :param str job_id: (optional) workspace JOB ID.
        :param str log_url: (optional) Log url for job.
        """
        self.workspace_id = workspace_id
        self.job_id = job_id
        self.resources_add = resources_add
        self.resources_modify = resources_modify
        self.resources_destroy = resources_destroy
        self.log_url = log_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryWorkitems':
        """Initialize a JobLogSummaryWorkitems object from a json dictionary."""
        args = {}
        if 'workspace_id' in _dict:
            args['workspace_id'] = _dict.get('workspace_id')
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        if 'resources_add' in _dict:
            args['resources_add'] = _dict.get('resources_add')
        if 'resources_modify' in _dict:
            args['resources_modify'] = _dict.get('resources_modify')
        if 'resources_destroy' in _dict:
            args['resources_destroy'] = _dict.get('resources_destroy')
        if 'log_url' in _dict:
            args['log_url'] = _dict.get('log_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryWorkitems object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'workspace_id') and self.workspace_id is not None:
            _dict['workspace_id'] = self.workspace_id
        if hasattr(self, 'job_id') and self.job_id is not None:
            _dict['job_id'] = self.job_id
        if hasattr(self, 'resources_add') and getattr(self, 'resources_add') is not None:
            _dict['resources_add'] = getattr(self, 'resources_add')
        if hasattr(self, 'resources_modify') and getattr(self, 'resources_modify') is not None:
            _dict['resources_modify'] = getattr(self, 'resources_modify')
        if hasattr(self, 'resources_destroy') and getattr(self, 'resources_destroy') is not None:
            _dict['resources_destroy'] = getattr(self, 'resources_destroy')
        if hasattr(self, 'log_url') and self.log_url is not None:
            _dict['log_url'] = self.log_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryWorkitems object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryWorkitems') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryWorkitems') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryActionJob():
    """
    Flow Job log summary.

    :attr float target_count: (optional) number of targets or hosts.
    :attr float task_count: (optional) number of tasks in playbook.
    :attr float play_count: (optional) number of plays in playbook.
    :attr JobLogSummaryActionJobRecap recap: (optional) Recap records.
    """

    def __init__(self,
                 *,
                 target_count: float = None,
                 task_count: float = None,
                 play_count: float = None,
                 recap: 'JobLogSummaryActionJobRecap' = None) -> None:
        """
        Initialize a JobLogSummaryActionJob object.

        :param JobLogSummaryActionJobRecap recap: (optional) Recap records.
        """
        self.target_count = target_count
        self.task_count = task_count
        self.play_count = play_count
        self.recap = recap

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryActionJob':
        """Initialize a JobLogSummaryActionJob object from a json dictionary."""
        args = {}
        if 'target_count' in _dict:
            args['target_count'] = _dict.get('target_count')
        if 'task_count' in _dict:
            args['task_count'] = _dict.get('task_count')
        if 'play_count' in _dict:
            args['play_count'] = _dict.get('play_count')
        if 'recap' in _dict:
            args['recap'] = JobLogSummaryActionJobRecap.from_dict(_dict.get('recap'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryActionJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'target_count') and getattr(self, 'target_count') is not None:
            _dict['target_count'] = getattr(self, 'target_count')
        if hasattr(self, 'task_count') and getattr(self, 'task_count') is not None:
            _dict['task_count'] = getattr(self, 'task_count')
        if hasattr(self, 'play_count') and getattr(self, 'play_count') is not None:
            _dict['play_count'] = getattr(self, 'play_count')
        if hasattr(self, 'recap') and self.recap is not None:
            _dict['recap'] = self.recap.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryActionJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryActionJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryActionJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryActionJobRecap():
    """
    Recap records.

    :attr List[str] target: (optional) List of target or host name.
    :attr float ok: (optional) Number of OK.
    :attr float changed: (optional) Number of changed.
    :attr float failed: (optional) Number of failed.
    :attr float skipped: (optional) Number of skipped.
    :attr float unreachable: (optional) Number of unreachable.
    """

    def __init__(self,
                 *,
                 target: List[str] = None,
                 ok: float = None,
                 changed: float = None,
                 failed: float = None,
                 skipped: float = None,
                 unreachable: float = None) -> None:
        """
        Initialize a JobLogSummaryActionJobRecap object.

        :param List[str] target: (optional) List of target or host name.
        :param float ok: (optional) Number of OK.
        :param float changed: (optional) Number of changed.
        :param float failed: (optional) Number of failed.
        :param float skipped: (optional) Number of skipped.
        :param float unreachable: (optional) Number of unreachable.
        """
        self.target = target
        self.ok = ok
        self.changed = changed
        self.failed = failed
        self.skipped = skipped
        self.unreachable = unreachable

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryActionJobRecap':
        """Initialize a JobLogSummaryActionJobRecap object from a json dictionary."""
        args = {}
        if 'target' in _dict:
            args['target'] = _dict.get('target')
        if 'ok' in _dict:
            args['ok'] = _dict.get('ok')
        if 'changed' in _dict:
            args['changed'] = _dict.get('changed')
        if 'failed' in _dict:
            args['failed'] = _dict.get('failed')
        if 'skipped' in _dict:
            args['skipped'] = _dict.get('skipped')
        if 'unreachable' in _dict:
            args['unreachable'] = _dict.get('unreachable')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryActionJobRecap object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'target') and self.target is not None:
            _dict['target'] = self.target
        if hasattr(self, 'ok') and self.ok is not None:
            _dict['ok'] = self.ok
        if hasattr(self, 'changed') and self.changed is not None:
            _dict['changed'] = self.changed
        if hasattr(self, 'failed') and self.failed is not None:
            _dict['failed'] = self.failed
        if hasattr(self, 'skipped') and self.skipped is not None:
            _dict['skipped'] = self.skipped
        if hasattr(self, 'unreachable') and self.unreachable is not None:
            _dict['unreachable'] = self.unreachable
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryActionJobRecap object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryActionJobRecap') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryActionJobRecap') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryFlowJob():
    """
    Flow Job log summary.

    :attr float workitems_completed: (optional) Number of workitems completed
          successfully.
    :attr float workitems_pending: (optional) Number of workitems pending in the
          flow.
    :attr float workitems_failed: (optional) Number of workitems failed.
    :attr List[JobLogSummaryWorkitems] workitems: (optional)
    """

    def __init__(self,
                 *,
                 workitems_completed: float = None,
                 workitems_pending: float = None,
                 workitems_failed: float = None,
                 workitems: List['JobLogSummaryWorkitems'] = None) -> None:
        """
        Initialize a JobLogSummaryFlowJob object.

        :param List[JobLogSummaryWorkitems] workitems: (optional)
        """
        self.workitems_completed = workitems_completed
        self.workitems_pending = workitems_pending
        self.workitems_failed = workitems_failed
        self.workitems = workitems

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryFlowJob':
        """Initialize a JobLogSummaryFlowJob object from a json dictionary."""
        args = {}
        if 'workitems_completed' in _dict:
            args['workitems_completed'] = _dict.get('workitems_completed')
        if 'workitems_pending' in _dict:
            args['workitems_pending'] = _dict.get('workitems_pending')
        if 'workitems_failed' in _dict:
            args['workitems_failed'] = _dict.get('workitems_failed')
        if 'workitems' in _dict:
            args['workitems'] = [JobLogSummaryWorkitems.from_dict(x) for x in _dict.get('workitems')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryFlowJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'workitems_completed') and getattr(self, 'workitems_completed') is not None:
            _dict['workitems_completed'] = getattr(self, 'workitems_completed')
        if hasattr(self, 'workitems_pending') and getattr(self, 'workitems_pending') is not None:
            _dict['workitems_pending'] = getattr(self, 'workitems_pending')
        if hasattr(self, 'workitems_failed') and getattr(self, 'workitems_failed') is not None:
            _dict['workitems_failed'] = getattr(self, 'workitems_failed')
        if hasattr(self, 'workitems') and self.workitems is not None:
            _dict['workitems'] = [x.to_dict() for x in self.workitems]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryFlowJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryFlowJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryFlowJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryLogErrors():
    """
    JobLogSummaryLogErrors.

    :attr str error_code: (optional) Error code in the Log.
    :attr str error_msg: (optional) Summary error message in the log.
    :attr float error_count: (optional) Number of occurrence.
    """

    def __init__(self,
                 *,
                 error_code: str = None,
                 error_msg: str = None,
                 error_count: float = None) -> None:
        """
        Initialize a JobLogSummaryLogErrors object.

        :param str error_code: (optional) Error code in the Log.
        :param str error_msg: (optional) Summary error message in the log.
        :param float error_count: (optional) Number of occurrence.
        """
        self.error_code = error_code
        self.error_msg = error_msg
        self.error_count = error_count

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryLogErrors':
        """Initialize a JobLogSummaryLogErrors object from a json dictionary."""
        args = {}
        if 'error_code' in _dict:
            args['error_code'] = _dict.get('error_code')
        if 'error_msg' in _dict:
            args['error_msg'] = _dict.get('error_msg')
        if 'error_count' in _dict:
            args['error_count'] = _dict.get('error_count')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryLogErrors object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'error_code') and self.error_code is not None:
            _dict['error_code'] = self.error_code
        if hasattr(self, 'error_msg') and self.error_msg is not None:
            _dict['error_msg'] = self.error_msg
        if hasattr(self, 'error_count') and self.error_count is not None:
            _dict['error_count'] = self.error_count
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryLogErrors object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryLogErrors') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryLogErrors') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryRepoDownloadJob():
    """
    Repo download Job log summary.

    :attr float scanned_file_count: (optional) Number of files scanned.
    :attr float quarantined_file_count: (optional) Number of files quarantined.
    :attr str detected_filetype: (optional) Detected template or data file type.
    :attr str inputs_count: (optional) Number of inputs detected.
    :attr str outputs_count: (optional) Number of outputs detected.
    """

    def __init__(self,
                 *,
                 scanned_file_count: float = None,
                 quarantined_file_count: float = None,
                 detected_filetype: str = None,
                 inputs_count: str = None,
                 outputs_count: str = None) -> None:
        """
        Initialize a JobLogSummaryRepoDownloadJob object.

        """
        self.scanned_file_count = scanned_file_count
        self.quarantined_file_count = quarantined_file_count
        self.detected_filetype = detected_filetype
        self.inputs_count = inputs_count
        self.outputs_count = outputs_count

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryRepoDownloadJob':
        """Initialize a JobLogSummaryRepoDownloadJob object from a json dictionary."""
        args = {}
        if 'scanned_file_count' in _dict:
            args['scanned_file_count'] = _dict.get('scanned_file_count')
        if 'quarantined_file_count' in _dict:
            args['quarantined_file_count'] = _dict.get('quarantined_file_count')
        if 'detected_filetype' in _dict:
            args['detected_filetype'] = _dict.get('detected_filetype')
        if 'inputs_count' in _dict:
            args['inputs_count'] = _dict.get('inputs_count')
        if 'outputs_count' in _dict:
            args['outputs_count'] = _dict.get('outputs_count')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryRepoDownloadJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'scanned_file_count') and getattr(self, 'scanned_file_count') is not None:
            _dict['scanned_file_count'] = getattr(self, 'scanned_file_count')
        if hasattr(self, 'quarantined_file_count') and getattr(self, 'quarantined_file_count') is not None:
            _dict['quarantined_file_count'] = getattr(self, 'quarantined_file_count')
        if hasattr(self, 'detected_filetype') and getattr(self, 'detected_filetype') is not None:
            _dict['detected_filetype'] = getattr(self, 'detected_filetype')
        if hasattr(self, 'inputs_count') and getattr(self, 'inputs_count') is not None:
            _dict['inputs_count'] = getattr(self, 'inputs_count')
        if hasattr(self, 'outputs_count') and getattr(self, 'outputs_count') is not None:
            _dict['outputs_count'] = getattr(self, 'outputs_count')
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryRepoDownloadJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryRepoDownloadJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryRepoDownloadJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummarySystemJob():
    """
    System Job log summary.

    :attr float target_count: (optional) number of targets or hosts.
    :attr float success: (optional) Number of passed.
    :attr float failed: (optional) Number of failed.
    """

    def __init__(self,
                 *,
                 target_count: float = None,
                 success: float = None,
                 failed: float = None) -> None:
        """
        Initialize a JobLogSummarySystemJob object.

        :param float success: (optional) Number of passed.
        :param float failed: (optional) Number of failed.
        """
        self.target_count = target_count
        self.success = success
        self.failed = failed

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummarySystemJob':
        """Initialize a JobLogSummarySystemJob object from a json dictionary."""
        args = {}
        if 'target_count' in _dict:
            args['target_count'] = _dict.get('target_count')
        if 'success' in _dict:
            args['success'] = _dict.get('success')
        if 'failed' in _dict:
            args['failed'] = _dict.get('failed')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummarySystemJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'target_count') and getattr(self, 'target_count') is not None:
            _dict['target_count'] = getattr(self, 'target_count')
        if hasattr(self, 'success') and self.success is not None:
            _dict['success'] = self.success
        if hasattr(self, 'failed') and self.failed is not None:
            _dict['failed'] = self.failed
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummarySystemJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummarySystemJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummarySystemJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobLogSummaryWorkspaceJob():
    """
    Workspace Job log summary.

    :attr float resources_add: (optional) Number of resources add.
    :attr float resources_modify: (optional) Number of resources modify.
    :attr float resources_destroy: (optional) Number of resources destroy.
    """

    def __init__(self,
                 *,
                 resources_add: float = None,
                 resources_modify: float = None,
                 resources_destroy: float = None) -> None:
        """
        Initialize a JobLogSummaryWorkspaceJob object.

        """
        self.resources_add = resources_add
        self.resources_modify = resources_modify
        self.resources_destroy = resources_destroy

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobLogSummaryWorkspaceJob':
        """Initialize a JobLogSummaryWorkspaceJob object from a json dictionary."""
        args = {}
        if 'resources_add' in _dict:
            args['resources_add'] = _dict.get('resources_add')
        if 'resources_modify' in _dict:
            args['resources_modify'] = _dict.get('resources_modify')
        if 'resources_destroy' in _dict:
            args['resources_destroy'] = _dict.get('resources_destroy')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobLogSummaryWorkspaceJob object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'resources_add') and getattr(self, 'resources_add') is not None:
            _dict['resources_add'] = getattr(self, 'resources_add')
        if hasattr(self, 'resources_modify') and getattr(self, 'resources_modify') is not None:
            _dict['resources_modify'] = getattr(self, 'resources_modify')
        if hasattr(self, 'resources_destroy') and getattr(self, 'resources_destroy') is not None:
            _dict['resources_destroy'] = getattr(self, 'resources_destroy')
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobLogSummaryWorkspaceJob object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobLogSummaryWorkspaceJob') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobLogSummaryWorkspaceJob') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobStatus():
    """
    Job Status.

    :attr JobStatusWorkspace workspace_job_status: (optional) Workspace Job Status.
    :attr JobStatusAction action_job_status: (optional) Action Job Status.
    :attr JobStatusSystem system_job_status: (optional) System Job Status.
    :attr JobStatusFlow flow_job_status: (optional) Environment Flow JOB Status.
    """

    def __init__(self,
                 *,
                 workspace_job_status: 'JobStatusWorkspace' = None,
                 action_job_status: 'JobStatusAction' = None,
                 system_job_status: 'JobStatusSystem' = None,
                 flow_job_status: 'JobStatusFlow' = None) -> None:
        """
        Initialize a JobStatus object.

        :param JobStatusWorkspace workspace_job_status: (optional) Workspace Job
               Status.
        :param JobStatusAction action_job_status: (optional) Action Job Status.
        :param JobStatusSystem system_job_status: (optional) System Job Status.
        :param JobStatusFlow flow_job_status: (optional) Environment Flow JOB
               Status.
        """
        self.workspace_job_status = workspace_job_status
        self.action_job_status = action_job_status
        self.system_job_status = system_job_status
        self.flow_job_status = flow_job_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatus':
        """Initialize a JobStatus object from a json dictionary."""
        args = {}
        if 'workspace_job_status' in _dict:
            args['workspace_job_status'] = JobStatusWorkspace.from_dict(_dict.get('workspace_job_status'))
        if 'action_job_status' in _dict:
            args['action_job_status'] = JobStatusAction.from_dict(_dict.get('action_job_status'))
        if 'system_job_status' in _dict:
            args['system_job_status'] = JobStatusSystem.from_dict(_dict.get('system_job_status'))
        if 'flow_job_status' in _dict:
            args['flow_job_status'] = JobStatusFlow.from_dict(_dict.get('flow_job_status'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatus object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'workspace_job_status') and self.workspace_job_status is not None:
            _dict['workspace_job_status'] = self.workspace_job_status.to_dict()
        if hasattr(self, 'action_job_status') and self.action_job_status is not None:
            _dict['action_job_status'] = self.action_job_status.to_dict()
        if hasattr(self, 'system_job_status') and self.system_job_status is not None:
            _dict['system_job_status'] = self.system_job_status.to_dict()
        if hasattr(self, 'flow_job_status') and self.flow_job_status is not None:
            _dict['flow_job_status'] = self.flow_job_status.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatus object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatus') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatus') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class JobStatusAction():
    """
    Action Job Status.

    :attr str action_name: (optional) Action name.
    :attr str status_code: (optional) Status of Jobs.
    :attr str status_message: (optional) Action Job status message - to be displayed
          along with the action_status_code.
    :attr str bastion_status_code: (optional) Status of Resources.
    :attr str bastion_status_message: (optional) Bastion status message - to be
          displayed along with the bastion_status_code;.
    :attr str targets_status_code: (optional) Status of Resources.
    :attr str targets_status_message: (optional) Aggregated status message for all
          target resources,  to be displayed along with the targets_status_code;.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 action_name: str = None,
                 status_code: str = None,
                 status_message: str = None,
                 bastion_status_code: str = None,
                 bastion_status_message: str = None,
                 targets_status_code: str = None,
                 targets_status_message: str = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusAction object.

        :param str action_name: (optional) Action name.
        :param str status_code: (optional) Status of Jobs.
        :param str status_message: (optional) Action Job status message - to be
               displayed along with the action_status_code.
        :param str bastion_status_code: (optional) Status of Resources.
        :param str bastion_status_message: (optional) Bastion status message - to
               be displayed along with the bastion_status_code;.
        :param str targets_status_code: (optional) Status of Resources.
        :param str targets_status_message: (optional) Aggregated status message for
               all target resources,  to be displayed along with the targets_status_code;.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.action_name = action_name
        self.status_code = status_code
        self.status_message = status_message
        self.bastion_status_code = bastion_status_code
        self.bastion_status_message = bastion_status_message
        self.targets_status_code = targets_status_code
        self.targets_status_message = targets_status_message
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusAction':
        """Initialize a JobStatusAction object from a json dictionary."""
        args = {}
        if 'action_name' in _dict:
            args['action_name'] = _dict.get('action_name')
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        if 'bastion_status_code' in _dict:
            args['bastion_status_code'] = _dict.get('bastion_status_code')
        if 'bastion_status_message' in _dict:
            args['bastion_status_message'] = _dict.get('bastion_status_message')
        if 'targets_status_code' in _dict:
            args['targets_status_code'] = _dict.get('targets_status_code')
        if 'targets_status_message' in _dict:
            args['targets_status_message'] = _dict.get('targets_status_message')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusAction object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_name') and self.action_name is not None:
            _dict['action_name'] = self.action_name
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        if hasattr(self, 'bastion_status_code') and self.bastion_status_code is not None:
            _dict['bastion_status_code'] = self.bastion_status_code
        if hasattr(self, 'bastion_status_message') and self.bastion_status_message is not None:
            _dict['bastion_status_message'] = self.bastion_status_message
        if hasattr(self, 'targets_status_code') and self.targets_status_code is not None:
            _dict['targets_status_code'] = self.targets_status_code
        if hasattr(self, 'targets_status_message') and self.targets_status_message is not None:
            _dict['targets_status_message'] = self.targets_status_message
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusAction object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusAction') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusAction') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        JOB_FINISHED = 'job_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


    class BastionStatusCodeEnum(str, Enum):
        """
        Status of Resources.
        """
        NONE = 'none'
        READY = 'ready'
        PROCESSING = 'processing'
        ERROR = 'error'


    class TargetsStatusCodeEnum(str, Enum):
        """
        Status of Resources.
        """
        NONE = 'none'
        READY = 'ready'
        PROCESSING = 'processing'
        ERROR = 'error'


class JobStatusFlow():
    """
    Environment Flow JOB Status.

    :attr str flow_id: (optional) flow id.
    :attr str flow_name: (optional) flow name.
    :attr str status_code: (optional) Status of Jobs.
    :attr str status_message: (optional) Flow Job status message - to be displayed
          along with the status_code;.
    :attr List[JobStatusWorkitem] workitems: (optional) Environment's individual
          workItem status details;.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 flow_id: str = None,
                 flow_name: str = None,
                 status_code: str = None,
                 status_message: str = None,
                 workitems: List['JobStatusWorkitem'] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusFlow object.

        :param str flow_id: (optional) flow id.
        :param str flow_name: (optional) flow name.
        :param str status_code: (optional) Status of Jobs.
        :param str status_message: (optional) Flow Job status message - to be
               displayed along with the status_code;.
        :param List[JobStatusWorkitem] workitems: (optional) Environment's
               individual workItem status details;.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.flow_id = flow_id
        self.flow_name = flow_name
        self.status_code = status_code
        self.status_message = status_message
        self.workitems = workitems
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusFlow':
        """Initialize a JobStatusFlow object from a json dictionary."""
        args = {}
        if 'flow_id' in _dict:
            args['flow_id'] = _dict.get('flow_id')
        if 'flow_name' in _dict:
            args['flow_name'] = _dict.get('flow_name')
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        if 'workitems' in _dict:
            args['workitems'] = [JobStatusWorkitem.from_dict(x) for x in _dict.get('workitems')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusFlow object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'flow_id') and self.flow_id is not None:
            _dict['flow_id'] = self.flow_id
        if hasattr(self, 'flow_name') and self.flow_name is not None:
            _dict['flow_name'] = self.flow_name
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        if hasattr(self, 'workitems') and self.workitems is not None:
            _dict['workitems'] = [x.to_dict() for x in self.workitems]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusFlow object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusFlow') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusFlow') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        JOB_FINISHED = 'job_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class JobStatusSchematicsResources():
    """
    schematics Resources Job Status.

    :attr str status_code: (optional) Status of Jobs.
    :attr str status_message: (optional) system job status message.
    :attr str schematics_resource_id: (optional) id for each resource which is
          targeted as a part of system job.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 status_code: str = None,
                 status_message: str = None,
                 schematics_resource_id: str = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusSchematicsResources object.

        :param str status_code: (optional) Status of Jobs.
        :param str status_message: (optional) system job status message.
        :param str schematics_resource_id: (optional) id for each resource which is
               targeted as a part of system job.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.status_code = status_code
        self.status_message = status_message
        self.schematics_resource_id = schematics_resource_id
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusSchematicsResources':
        """Initialize a JobStatusSchematicsResources object from a json dictionary."""
        args = {}
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        if 'schematics_resource_id' in _dict:
            args['schematics_resource_id'] = _dict.get('schematics_resource_id')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusSchematicsResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        if hasattr(self, 'schematics_resource_id') and self.schematics_resource_id is not None:
            _dict['schematics_resource_id'] = self.schematics_resource_id
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusSchematicsResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusSchematicsResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusSchematicsResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        JOB_FINISHED = 'job_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class JobStatusSystem():
    """
    System Job Status.

    :attr str system_status_message: (optional) System job message.
    :attr str system_status_code: (optional) Status of Jobs.
    :attr List[JobStatusSchematicsResources] schematics_resource_status: (optional)
          job staus for each schematics resource.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 system_status_message: str = None,
                 system_status_code: str = None,
                 schematics_resource_status: List['JobStatusSchematicsResources'] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusSystem object.

        :param str system_status_message: (optional) System job message.
        :param str system_status_code: (optional) Status of Jobs.
        :param List[JobStatusSchematicsResources] schematics_resource_status:
               (optional) job staus for each schematics resource.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.system_status_message = system_status_message
        self.system_status_code = system_status_code
        self.schematics_resource_status = schematics_resource_status
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusSystem':
        """Initialize a JobStatusSystem object from a json dictionary."""
        args = {}
        if 'system_status_message' in _dict:
            args['system_status_message'] = _dict.get('system_status_message')
        if 'system_status_code' in _dict:
            args['system_status_code'] = _dict.get('system_status_code')
        if 'schematics_resource_status' in _dict:
            args['schematics_resource_status'] = [JobStatusSchematicsResources.from_dict(x) for x in _dict.get('schematics_resource_status')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusSystem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'system_status_message') and self.system_status_message is not None:
            _dict['system_status_message'] = self.system_status_message
        if hasattr(self, 'system_status_code') and self.system_status_code is not None:
            _dict['system_status_code'] = self.system_status_code
        if hasattr(self, 'schematics_resource_status') and self.schematics_resource_status is not None:
            _dict['schematics_resource_status'] = [x.to_dict() for x in self.schematics_resource_status]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusSystem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusSystem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusSystem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class SystemStatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        JOB_FINISHED = 'job_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class JobStatusTemplate():
    """
    Template Job Status.

    :attr str template_id: (optional) Template Id.
    :attr str template_name: (optional) Template name.
    :attr int flow_index: (optional) Index of the template in the Flow.
    :attr str status_code: (optional) Status of Jobs.
    :attr str status_message: (optional) Template job status message (eg.
          VPCt1_Apply_Pending, for a 'VPCt1' Template).
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 template_id: str = None,
                 template_name: str = None,
                 flow_index: int = None,
                 status_code: str = None,
                 status_message: str = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusTemplate object.

        :param str template_id: (optional) Template Id.
        :param str template_name: (optional) Template name.
        :param int flow_index: (optional) Index of the template in the Flow.
        :param str status_code: (optional) Status of Jobs.
        :param str status_message: (optional) Template job status message (eg.
               VPCt1_Apply_Pending, for a 'VPCt1' Template).
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.template_id = template_id
        self.template_name = template_name
        self.flow_index = flow_index
        self.status_code = status_code
        self.status_message = status_message
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusTemplate':
        """Initialize a JobStatusTemplate object from a json dictionary."""
        args = {}
        if 'template_id' in _dict:
            args['template_id'] = _dict.get('template_id')
        if 'template_name' in _dict:
            args['template_name'] = _dict.get('template_name')
        if 'flow_index' in _dict:
            args['flow_index'] = _dict.get('flow_index')
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusTemplate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'template_id') and self.template_id is not None:
            _dict['template_id'] = self.template_id
        if hasattr(self, 'template_name') and self.template_name is not None:
            _dict['template_name'] = self.template_name
        if hasattr(self, 'flow_index') and self.flow_index is not None:
            _dict['flow_index'] = self.flow_index
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusTemplate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusTemplate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusTemplate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        JOB_FINISHED = 'job_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class JobStatusWorkitem():
    """
    Individual workitem status info.

    :attr str workspace_id: (optional) Workspace id.
    :attr str workspace_name: (optional) workspace name.
    :attr str job_id: (optional) workspace job id.
    :attr str status_code: (optional) Status of Jobs.
    :attr str status_message: (optional) workitem job status message;.
    :attr datetime updated_at: (optional) workitem job status updation timestamp.
    """

    def __init__(self,
                 *,
                 workspace_id: str = None,
                 workspace_name: str = None,
                 job_id: str = None,
                 status_code: str = None,
                 status_message: str = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusWorkitem object.

        :param str workspace_id: (optional) Workspace id.
        :param str workspace_name: (optional) workspace name.
        :param str job_id: (optional) workspace job id.
        :param str status_code: (optional) Status of Jobs.
        :param str status_message: (optional) workitem job status message;.
        :param datetime updated_at: (optional) workitem job status updation
               timestamp.
        """
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        self.job_id = job_id
        self.status_code = status_code
        self.status_message = status_message
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusWorkitem':
        """Initialize a JobStatusWorkitem object from a json dictionary."""
        args = {}
        if 'workspace_id' in _dict:
            args['workspace_id'] = _dict.get('workspace_id')
        if 'workspace_name' in _dict:
            args['workspace_name'] = _dict.get('workspace_name')
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusWorkitem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'workspace_id') and self.workspace_id is not None:
            _dict['workspace_id'] = self.workspace_id
        if hasattr(self, 'workspace_name') and self.workspace_name is not None:
            _dict['workspace_name'] = self.workspace_name
        if hasattr(self, 'job_id') and self.job_id is not None:
            _dict['job_id'] = self.job_id
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusWorkitem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusWorkitem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusWorkitem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        JOB_FINISHED = 'job_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class JobStatusWorkspace():
    """
    Workspace Job Status.

    :attr str workspace_name: (optional) Workspace name.
    :attr str status_code: (optional) Status of Jobs.
    :attr str status_message: (optional) Workspace job status message (eg.
          App1_Setup_Pending, for a 'Setup' flow in the 'App1' Workspace).
    :attr JobStatusFlow flow_status: (optional) Environment Flow JOB Status.
    :attr List[JobStatusTemplate] template_status: (optional) Workspace Flow
          Template job status.
    :attr datetime updated_at: (optional) Job status updation timestamp.
    """

    def __init__(self,
                 *,
                 workspace_name: str = None,
                 status_code: str = None,
                 status_message: str = None,
                 flow_status: 'JobStatusFlow' = None,
                 template_status: List['JobStatusTemplate'] = None,
                 updated_at: datetime = None) -> None:
        """
        Initialize a JobStatusWorkspace object.

        :param str workspace_name: (optional) Workspace name.
        :param str status_code: (optional) Status of Jobs.
        :param str status_message: (optional) Workspace job status message (eg.
               App1_Setup_Pending, for a 'Setup' flow in the 'App1' Workspace).
        :param JobStatusFlow flow_status: (optional) Environment Flow JOB Status.
        :param List[JobStatusTemplate] template_status: (optional) Workspace Flow
               Template job status.
        :param datetime updated_at: (optional) Job status updation timestamp.
        """
        self.workspace_name = workspace_name
        self.status_code = status_code
        self.status_message = status_message
        self.flow_status = flow_status
        self.template_status = template_status
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'JobStatusWorkspace':
        """Initialize a JobStatusWorkspace object from a json dictionary."""
        args = {}
        if 'workspace_name' in _dict:
            args['workspace_name'] = _dict.get('workspace_name')
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_message' in _dict:
            args['status_message'] = _dict.get('status_message')
        if 'flow_status' in _dict:
            args['flow_status'] = JobStatusFlow.from_dict(_dict.get('flow_status'))
        if 'template_status' in _dict:
            args['template_status'] = [JobStatusTemplate.from_dict(x) for x in _dict.get('template_status')]
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a JobStatusWorkspace object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'workspace_name') and self.workspace_name is not None:
            _dict['workspace_name'] = self.workspace_name
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_message') and self.status_message is not None:
            _dict['status_message'] = self.status_message
        if hasattr(self, 'flow_status') and self.flow_status is not None:
            _dict['flow_status'] = self.flow_status.to_dict()
        if hasattr(self, 'template_status') and self.template_status is not None:
            _dict['template_status'] = [x.to_dict() for x in self.template_status]
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this JobStatusWorkspace object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'JobStatusWorkspace') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'JobStatusWorkspace') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StatusCodeEnum(str, Enum):
        """
        Status of Jobs.
        """
        JOB_PENDING = 'job_pending'
        JOB_IN_PROGRESS = 'job_in_progress'
        JOB_FINISHED = 'job_finished'
        JOB_FAILED = 'job_failed'
        JOB_CANCELLED = 'job_cancelled'


class KMSDiscovery():
    """
    Discovered KMS instances.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[KMSInstances] kms_instances: (optional) List of KMS instances.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 kms_instances: List['KMSInstances'] = None) -> None:
        """
        Initialize a KMSDiscovery object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[KMSInstances] kms_instances: (optional) List of KMS instances.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.kms_instances = kms_instances

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSDiscovery':
        """Initialize a KMSDiscovery object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in KMSDiscovery JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in KMSDiscovery JSON')
        if 'kms_instances' in _dict:
            args['kms_instances'] = [KMSInstances.from_dict(x) for x in _dict.get('kms_instances')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSDiscovery object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'kms_instances') and self.kms_instances is not None:
            _dict['kms_instances'] = [x.to_dict() for x in self.kms_instances]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSDiscovery object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSDiscovery') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSDiscovery') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSInstances():
    """
    KMS Instances.

    :attr str location: (optional) Location.
    :attr str encryption_scheme: (optional) Encryption schema.
    :attr str resource_group: (optional) Resource groups.
    :attr str kms_crn: (optional) KMS CRN.
    :attr str kms_name: (optional) KMS Name.
    :attr str kms_private_endpoint: (optional) KMS private endpoint.
    :attr str kms_public_endpoint: (optional) KMS public endpoint.
    :attr List[KMSInstancesKeys] keys: (optional) List of keys.
    """

    def __init__(self,
                 *,
                 location: str = None,
                 encryption_scheme: str = None,
                 resource_group: str = None,
                 kms_crn: str = None,
                 kms_name: str = None,
                 kms_private_endpoint: str = None,
                 kms_public_endpoint: str = None,
                 keys: List['KMSInstancesKeys'] = None) -> None:
        """
        Initialize a KMSInstances object.

        :param str location: (optional) Location.
        :param str encryption_scheme: (optional) Encryption schema.
        :param str resource_group: (optional) Resource groups.
        :param str kms_crn: (optional) KMS CRN.
        :param str kms_name: (optional) KMS Name.
        :param str kms_private_endpoint: (optional) KMS private endpoint.
        :param str kms_public_endpoint: (optional) KMS public endpoint.
        :param List[KMSInstancesKeys] keys: (optional) List of keys.
        """
        self.location = location
        self.encryption_scheme = encryption_scheme
        self.resource_group = resource_group
        self.kms_crn = kms_crn
        self.kms_name = kms_name
        self.kms_private_endpoint = kms_private_endpoint
        self.kms_public_endpoint = kms_public_endpoint
        self.keys = keys

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSInstances':
        """Initialize a KMSInstances object from a json dictionary."""
        args = {}
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'encryption_scheme' in _dict:
            args['encryption_scheme'] = _dict.get('encryption_scheme')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'kms_crn' in _dict:
            args['kms_crn'] = _dict.get('kms_crn')
        if 'kms_name' in _dict:
            args['kms_name'] = _dict.get('kms_name')
        if 'kms_private_endpoint' in _dict:
            args['kms_private_endpoint'] = _dict.get('kms_private_endpoint')
        if 'kms_public_endpoint' in _dict:
            args['kms_public_endpoint'] = _dict.get('kms_public_endpoint')
        if 'keys' in _dict:
            args['keys'] = [KMSInstancesKeys.from_dict(x) for x in _dict.get('keys')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSInstances object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'encryption_scheme') and self.encryption_scheme is not None:
            _dict['encryption_scheme'] = self.encryption_scheme
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'kms_crn') and self.kms_crn is not None:
            _dict['kms_crn'] = self.kms_crn
        if hasattr(self, 'kms_name') and self.kms_name is not None:
            _dict['kms_name'] = self.kms_name
        if hasattr(self, 'kms_private_endpoint') and self.kms_private_endpoint is not None:
            _dict['kms_private_endpoint'] = self.kms_private_endpoint
        if hasattr(self, 'kms_public_endpoint') and self.kms_public_endpoint is not None:
            _dict['kms_public_endpoint'] = self.kms_public_endpoint
        if hasattr(self, 'keys') and self.keys is not None:
            _dict['keys'] = [x.to_dict() for x in self.keys]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSInstances object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSInstances') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSInstances') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSInstancesKeys():
    """
    KMSInstancesKeys.

    :attr str name: (optional) Key name.
    :attr str crn: (optional) CRN of the Key.
    :attr str error: (optional) Error message.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 crn: str = None,
                 error: str = None) -> None:
        """
        Initialize a KMSInstancesKeys object.

        :param str name: (optional) Key name.
        :param str crn: (optional) CRN of the Key.
        :param str error: (optional) Error message.
        """
        self.name = name
        self.crn = crn
        self.error = error

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSInstancesKeys':
        """Initialize a KMSInstancesKeys object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'error' in _dict:
            args['error'] = _dict.get('error')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSInstancesKeys object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['crn'] = self.crn
        if hasattr(self, 'error') and self.error is not None:
            _dict['error'] = self.error
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSInstancesKeys object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSInstancesKeys') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSInstancesKeys') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSSettings():
    """
    User defined KMS Settings details.

    :attr str location: (optional) Location.
    :attr str encryption_scheme: (optional) Encryption scheme.
    :attr str resource_group: (optional) Resource group.
    :attr KMSSettingsPrimaryCrk primary_crk: (optional) Primary CRK details.
    :attr KMSSettingsSecondaryCrk secondary_crk: (optional) Secondary CRK details.
    """

    def __init__(self,
                 *,
                 location: str = None,
                 encryption_scheme: str = None,
                 resource_group: str = None,
                 primary_crk: 'KMSSettingsPrimaryCrk' = None,
                 secondary_crk: 'KMSSettingsSecondaryCrk' = None) -> None:
        """
        Initialize a KMSSettings object.

        :param str location: (optional) Location.
        :param str encryption_scheme: (optional) Encryption scheme.
        :param str resource_group: (optional) Resource group.
        :param KMSSettingsPrimaryCrk primary_crk: (optional) Primary CRK details.
        :param KMSSettingsSecondaryCrk secondary_crk: (optional) Secondary CRK
               details.
        """
        self.location = location
        self.encryption_scheme = encryption_scheme
        self.resource_group = resource_group
        self.primary_crk = primary_crk
        self.secondary_crk = secondary_crk

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSSettings':
        """Initialize a KMSSettings object from a json dictionary."""
        args = {}
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'encryption_scheme' in _dict:
            args['encryption_scheme'] = _dict.get('encryption_scheme')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'primary_crk' in _dict:
            args['primary_crk'] = KMSSettingsPrimaryCrk.from_dict(_dict.get('primary_crk'))
        if 'secondary_crk' in _dict:
            args['secondary_crk'] = KMSSettingsSecondaryCrk.from_dict(_dict.get('secondary_crk'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSSettings object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'encryption_scheme') and self.encryption_scheme is not None:
            _dict['encryption_scheme'] = self.encryption_scheme
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'primary_crk') and self.primary_crk is not None:
            _dict['primary_crk'] = self.primary_crk.to_dict()
        if hasattr(self, 'secondary_crk') and self.secondary_crk is not None:
            _dict['secondary_crk'] = self.secondary_crk.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSSettings object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSSettings') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSSettings') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSSettingsPrimaryCrk():
    """
    Primary CRK details.

    :attr str kms_name: (optional) Primary KMS name.
    :attr str kms_private_endpoint: (optional) Primary KMS endpoint.
    :attr str key_crn: (optional) CRN of the Primary Key.
    """

    def __init__(self,
                 *,
                 kms_name: str = None,
                 kms_private_endpoint: str = None,
                 key_crn: str = None) -> None:
        """
        Initialize a KMSSettingsPrimaryCrk object.

        :param str kms_name: (optional) Primary KMS name.
        :param str kms_private_endpoint: (optional) Primary KMS endpoint.
        :param str key_crn: (optional) CRN of the Primary Key.
        """
        self.kms_name = kms_name
        self.kms_private_endpoint = kms_private_endpoint
        self.key_crn = key_crn

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSSettingsPrimaryCrk':
        """Initialize a KMSSettingsPrimaryCrk object from a json dictionary."""
        args = {}
        if 'kms_name' in _dict:
            args['kms_name'] = _dict.get('kms_name')
        if 'kms_private_endpoint' in _dict:
            args['kms_private_endpoint'] = _dict.get('kms_private_endpoint')
        if 'key_crn' in _dict:
            args['key_crn'] = _dict.get('key_crn')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSSettingsPrimaryCrk object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'kms_name') and self.kms_name is not None:
            _dict['kms_name'] = self.kms_name
        if hasattr(self, 'kms_private_endpoint') and self.kms_private_endpoint is not None:
            _dict['kms_private_endpoint'] = self.kms_private_endpoint
        if hasattr(self, 'key_crn') and self.key_crn is not None:
            _dict['key_crn'] = self.key_crn
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSSettingsPrimaryCrk object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSSettingsPrimaryCrk') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSSettingsPrimaryCrk') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class KMSSettingsSecondaryCrk():
    """
    Secondary CRK details.

    :attr str kms_name: (optional) Secondary KMS name.
    :attr str kms_private_endpoint: (optional) Secondary KMS endpoint.
    :attr str key_crn: (optional) CRN of the Secondary Key.
    """

    def __init__(self,
                 *,
                 kms_name: str = None,
                 kms_private_endpoint: str = None,
                 key_crn: str = None) -> None:
        """
        Initialize a KMSSettingsSecondaryCrk object.

        :param str kms_name: (optional) Secondary KMS name.
        :param str kms_private_endpoint: (optional) Secondary KMS endpoint.
        :param str key_crn: (optional) CRN of the Secondary Key.
        """
        self.kms_name = kms_name
        self.kms_private_endpoint = kms_private_endpoint
        self.key_crn = key_crn

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'KMSSettingsSecondaryCrk':
        """Initialize a KMSSettingsSecondaryCrk object from a json dictionary."""
        args = {}
        if 'kms_name' in _dict:
            args['kms_name'] = _dict.get('kms_name')
        if 'kms_private_endpoint' in _dict:
            args['kms_private_endpoint'] = _dict.get('kms_private_endpoint')
        if 'key_crn' in _dict:
            args['key_crn'] = _dict.get('key_crn')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a KMSSettingsSecondaryCrk object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'kms_name') and self.kms_name is not None:
            _dict['kms_name'] = self.kms_name
        if hasattr(self, 'kms_private_endpoint') and self.kms_private_endpoint is not None:
            _dict['kms_private_endpoint'] = self.kms_private_endpoint
        if hasattr(self, 'key_crn') and self.key_crn is not None:
            _dict['key_crn'] = self.key_crn
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this KMSSettingsSecondaryCrk object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'KMSSettingsSecondaryCrk') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'KMSSettingsSecondaryCrk') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class LogStoreResponse():
    """
    Log file URL for job that ran against your workspace.

    :attr str engine_name: (optional) The provisioning engine that was used for the
          job.
    :attr str engine_version: (optional) The version of the provisioning engine that
          was used for the job.
    :attr str id: (optional) The ID that was assigned to your Terraform template of
          IBM Cloud catalog software template.
    :attr str log_store_url: (optional) The URL to access the logs that were created
          during the plan, apply, or destroy job.
    """

    def __init__(self,
                 *,
                 engine_name: str = None,
                 engine_version: str = None,
                 id: str = None,
                 log_store_url: str = None) -> None:
        """
        Initialize a LogStoreResponse object.

        :param str engine_name: (optional) The provisioning engine that was used
               for the job.
        :param str engine_version: (optional) The version of the provisioning
               engine that was used for the job.
        :param str id: (optional) The ID that was assigned to your Terraform
               template of IBM Cloud catalog software template.
        :param str log_store_url: (optional) The URL to access the logs that were
               created during the plan, apply, or destroy job.
        """
        self.engine_name = engine_name
        self.engine_version = engine_version
        self.id = id
        self.log_store_url = log_store_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LogStoreResponse':
        """Initialize a LogStoreResponse object from a json dictionary."""
        args = {}
        if 'engine_name' in _dict:
            args['engine_name'] = _dict.get('engine_name')
        if 'engine_version' in _dict:
            args['engine_version'] = _dict.get('engine_version')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'log_store_url' in _dict:
            args['log_store_url'] = _dict.get('log_store_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LogStoreResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'engine_name') and self.engine_name is not None:
            _dict['engine_name'] = self.engine_name
        if hasattr(self, 'engine_version') and self.engine_version is not None:
            _dict['engine_version'] = self.engine_version
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'log_store_url') and self.log_store_url is not None:
            _dict['log_store_url'] = self.log_store_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LogStoreResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LogStoreResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LogStoreResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class LogStoreResponseList():
    """
    List of log file URL that ran against your workspace.

    :attr List[LogStoreResponse] runtime_data: (optional) Runtime data.
    """

    def __init__(self,
                 *,
                 runtime_data: List['LogStoreResponse'] = None) -> None:
        """
        Initialize a LogStoreResponseList object.

        :param List[LogStoreResponse] runtime_data: (optional) Runtime data.
        """
        self.runtime_data = runtime_data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LogStoreResponseList':
        """Initialize a LogStoreResponseList object from a json dictionary."""
        args = {}
        if 'runtime_data' in _dict:
            args['runtime_data'] = [LogStoreResponse.from_dict(x) for x in _dict.get('runtime_data')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LogStoreResponseList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'runtime_data') and self.runtime_data is not None:
            _dict['runtime_data'] = [x.to_dict() for x in self.runtime_data]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LogStoreResponseList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LogStoreResponseList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LogStoreResponseList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class LogSummary():
    """
    Summary information extracted from the job logs.

    :attr str activity_status: (optional) The status of your activity or job. To
          retrieve the URL to your job logs, use the GET
          /v1/workspaces/{id}/actions/{action_id}/logs API.
          * **COMPLETED**: The job completed successfully.
          * **CREATED**: The job was created, but the provisioning, modification, or
          removal of IBM Cloud resources has not started yet.
          * **FAILED**: An error occurred during the plan, apply, or destroy job. Use the
          job ID to retrieve the URL to the log files for your job.
          * **IN PROGRESS**: The job is in progress. You can use the log_url to access the
          logs.
    :attr str detected_template_type: (optional) Template detected type.
    :attr int discarded_files: (optional) Numner of discarded files.
    :attr str error: (optional) Numner of errors in log.
    :attr int resources_added: (optional) Numner of resources added.
    :attr int resources_destroyed: (optional) Numner of resources destroyed.
    :attr int resources_modified: (optional) Numner of resources modified.
    :attr int scanned_files: (optional) Numner of filed scanned.
    :attr int template_variable_count: (optional) Numner of template variables.
    :attr float time_taken: (optional) Elapsed time to run the job.
    """

    def __init__(self,
                 *,
                 activity_status: str = None,
                 detected_template_type: str = None,
                 discarded_files: int = None,
                 error: str = None,
                 resources_added: int = None,
                 resources_destroyed: int = None,
                 resources_modified: int = None,
                 scanned_files: int = None,
                 template_variable_count: int = None,
                 time_taken: float = None) -> None:
        """
        Initialize a LogSummary object.

        :param str activity_status: (optional) The status of your activity or job.
               To retrieve the URL to your job logs, use the GET
               /v1/workspaces/{id}/actions/{action_id}/logs API.
               * **COMPLETED**: The job completed successfully.
               * **CREATED**: The job was created, but the provisioning, modification, or
               removal of IBM Cloud resources has not started yet.
               * **FAILED**: An error occurred during the plan, apply, or destroy job. Use
               the job ID to retrieve the URL to the log files for your job.
               * **IN PROGRESS**: The job is in progress. You can use the log_url to
               access the logs.
        :param str detected_template_type: (optional) Template detected type.
        :param int discarded_files: (optional) Numner of discarded files.
        :param str error: (optional) Numner of errors in log.
        :param int resources_added: (optional) Numner of resources added.
        :param int resources_destroyed: (optional) Numner of resources destroyed.
        :param int resources_modified: (optional) Numner of resources modified.
        :param int scanned_files: (optional) Numner of filed scanned.
        :param int template_variable_count: (optional) Numner of template
               variables.
        :param float time_taken: (optional) Elapsed time to run the job.
        """
        self.activity_status = activity_status
        self.detected_template_type = detected_template_type
        self.discarded_files = discarded_files
        self.error = error
        self.resources_added = resources_added
        self.resources_destroyed = resources_destroyed
        self.resources_modified = resources_modified
        self.scanned_files = scanned_files
        self.template_variable_count = template_variable_count
        self.time_taken = time_taken

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LogSummary':
        """Initialize a LogSummary object from a json dictionary."""
        args = {}
        if 'activity_status' in _dict:
            args['activity_status'] = _dict.get('activity_status')
        if 'detected_template_type' in _dict:
            args['detected_template_type'] = _dict.get('detected_template_type')
        if 'discarded_files' in _dict:
            args['discarded_files'] = _dict.get('discarded_files')
        if 'error' in _dict:
            args['error'] = _dict.get('error')
        if 'resources_added' in _dict:
            args['resources_added'] = _dict.get('resources_added')
        if 'resources_destroyed' in _dict:
            args['resources_destroyed'] = _dict.get('resources_destroyed')
        if 'resources_modified' in _dict:
            args['resources_modified'] = _dict.get('resources_modified')
        if 'scanned_files' in _dict:
            args['scanned_files'] = _dict.get('scanned_files')
        if 'template_variable_count' in _dict:
            args['template_variable_count'] = _dict.get('template_variable_count')
        if 'time_taken' in _dict:
            args['time_taken'] = _dict.get('time_taken')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LogSummary object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activity_status') and self.activity_status is not None:
            _dict['activity_status'] = self.activity_status
        if hasattr(self, 'detected_template_type') and self.detected_template_type is not None:
            _dict['detected_template_type'] = self.detected_template_type
        if hasattr(self, 'discarded_files') and self.discarded_files is not None:
            _dict['discarded_files'] = self.discarded_files
        if hasattr(self, 'error') and self.error is not None:
            _dict['error'] = self.error
        if hasattr(self, 'resources_added') and self.resources_added is not None:
            _dict['resources_added'] = self.resources_added
        if hasattr(self, 'resources_destroyed') and self.resources_destroyed is not None:
            _dict['resources_destroyed'] = self.resources_destroyed
        if hasattr(self, 'resources_modified') and self.resources_modified is not None:
            _dict['resources_modified'] = self.resources_modified
        if hasattr(self, 'scanned_files') and self.scanned_files is not None:
            _dict['scanned_files'] = self.scanned_files
        if hasattr(self, 'template_variable_count') and self.template_variable_count is not None:
            _dict['template_variable_count'] = self.template_variable_count
        if hasattr(self, 'time_taken') and self.time_taken is not None:
            _dict['time_taken'] = self.time_taken
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LogSummary object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LogSummary') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LogSummary') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class OutputValuesInner():
    """
    OutputValuesInner.

    :attr str folder: (optional) The subfolder in the GitHub or GitLab repository
          where your Terraform template is stored. If the template is stored in the root
          directory, `.` is returned.
    :attr str id: (optional) The ID that was assigned to your Terraform template or
          IBM Cloud catalog software template.
    :attr List[object] output_values: (optional) A list of Terraform output values.
    :attr str value_type: (optional) The Terraform version that was used to apply
          your template.
    """

    def __init__(self,
                 *,
                 folder: str = None,
                 id: str = None,
                 output_values: List[object] = None,
                 value_type: str = None) -> None:
        """
        Initialize a OutputValuesInner object.

        :param str folder: (optional) The subfolder in the GitHub or GitLab
               repository where your Terraform template is stored. If the template is
               stored in the root directory, `.` is returned.
        :param str id: (optional) The ID that was assigned to your Terraform
               template or IBM Cloud catalog software template.
        :param List[object] output_values: (optional) A list of Terraform output
               values.
        :param str value_type: (optional) The Terraform version that was used to
               apply your template.
        """
        self.folder = folder
        self.id = id
        self.output_values = output_values
        self.value_type = value_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'OutputValuesInner':
        """Initialize a OutputValuesInner object from a json dictionary."""
        args = {}
        if 'folder' in _dict:
            args['folder'] = _dict.get('folder')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'output_values' in _dict:
            args['output_values'] = _dict.get('output_values')
        if 'value_type' in _dict:
            args['value_type'] = _dict.get('value_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a OutputValuesInner object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'folder') and self.folder is not None:
            _dict['folder'] = self.folder
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'output_values') and self.output_values is not None:
            _dict['output_values'] = self.output_values
        if hasattr(self, 'value_type') and self.value_type is not None:
            _dict['value_type'] = self.value_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this OutputValuesInner object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'OutputValuesInner') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'OutputValuesInner') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceGroupResponse():
    """
    A list of resource groups that your account has access to.

    :attr str account_id: (optional) The ID of the account for which you listed the
          resource groups.
    :attr str crn: (optional) The CRN of the resource group.
    :attr bool default: (optional) If set to **true**, the resource group is used as
          the default resource group for your account. If set to **false**, the resource
          group is not used as the default resource group in your account.
    :attr str name: (optional) The name of the resource group.
    :attr str resource_group_id: (optional) The ID of the resource group.
    :attr str state: (optional) The state of the resource group.
    """

    def __init__(self,
                 *,
                 account_id: str = None,
                 crn: str = None,
                 default: bool = None,
                 name: str = None,
                 resource_group_id: str = None,
                 state: str = None) -> None:
        """
        Initialize a ResourceGroupResponse object.

        :param str account_id: (optional) The ID of the account for which you
               listed the resource groups.
        :param str crn: (optional) The CRN of the resource group.
        :param bool default: (optional) If set to **true**, the resource group is
               used as the default resource group for your account. If set to **false**,
               the resource group is not used as the default resource group in your
               account.
        :param str name: (optional) The name of the resource group.
        :param str resource_group_id: (optional) The ID of the resource group.
        :param str state: (optional) The state of the resource group.
        """
        self.account_id = account_id
        self.crn = crn
        self.default = default
        self.name = name
        self.resource_group_id = resource_group_id
        self.state = state

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceGroupResponse':
        """Initialize a ResourceGroupResponse object from a json dictionary."""
        args = {}
        if 'account_id' in _dict:
            args['account_id'] = _dict.get('account_id')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'default' in _dict:
            args['default'] = _dict.get('default')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'resource_group_id' in _dict:
            args['resource_group_id'] = _dict.get('resource_group_id')
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceGroupResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'account_id') and self.account_id is not None:
            _dict['account_id'] = self.account_id
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['crn'] = self.crn
        if hasattr(self, 'default') and self.default is not None:
            _dict['default'] = self.default
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'resource_group_id') and self.resource_group_id is not None:
            _dict['resource_group_id'] = self.resource_group_id
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceGroupResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceGroupResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceGroupResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQuery():
    """
    Describe resource query.

    :attr str query_type: (optional) Type of the query(workspaces).
    :attr List[ResourceQueryParam] query_condition: (optional)
    :attr List[str] query_select: (optional) List of query selection parameters.
    """

    def __init__(self,
                 *,
                 query_type: str = None,
                 query_condition: List['ResourceQueryParam'] = None,
                 query_select: List[str] = None) -> None:
        """
        Initialize a ResourceQuery object.

        :param str query_type: (optional) Type of the query(workspaces).
        :param List[ResourceQueryParam] query_condition: (optional)
        :param List[str] query_select: (optional) List of query selection
               parameters.
        """
        self.query_type = query_type
        self.query_condition = query_condition
        self.query_select = query_select

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQuery':
        """Initialize a ResourceQuery object from a json dictionary."""
        args = {}
        if 'query_type' in _dict:
            args['query_type'] = _dict.get('query_type')
        if 'query_condition' in _dict:
            args['query_condition'] = [ResourceQueryParam.from_dict(x) for x in _dict.get('query_condition')]
        if 'query_select' in _dict:
            args['query_select'] = _dict.get('query_select')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQuery object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'query_type') and self.query_type is not None:
            _dict['query_type'] = self.query_type
        if hasattr(self, 'query_condition') and self.query_condition is not None:
            _dict['query_condition'] = [x.to_dict() for x in self.query_condition]
        if hasattr(self, 'query_select') and self.query_select is not None:
            _dict['query_select'] = self.query_select
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQuery object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQuery') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQuery') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class QueryTypeEnum(str, Enum):
        """
        Type of the query(workspaces).
        """
        WORKSPACES = 'workspaces'


class ResourceQueryParam():
    """
    Describe resource query param.

    :attr str name: (optional) Name of the resource query param.
    :attr str value: (optional) Value of the resource query param.
    :attr str description: (optional) Description of resource query param variable.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 value: str = None,
                 description: str = None) -> None:
        """
        Initialize a ResourceQueryParam object.

        :param str name: (optional) Name of the resource query param.
        :param str value: (optional) Value of the resource query param.
        :param str description: (optional) Description of resource query param
               variable.
        """
        self.name = name
        self.value = value
        self.description = description

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryParam':
        """Initialize a ResourceQueryParam object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryParam object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryParam object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryParam') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryParam') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQueryRecord():
    """
    Describe resource query record.

    :attr str type: (optional) Resource type (cluster, vsi, icd, vpc).
    :attr str name: (optional) Resource query name.
    :attr str id: (optional) Resource Query id.
    :attr datetime created_at: (optional) Resource query creation time.
    :attr str created_by: (optional) Email address of user who created the Resource
          query.
    :attr datetime updated_at: (optional) Resource query updation time.
    :attr str updated_by: (optional) Email address of user who updated the Resource
          query.
    :attr List[ResourceQuery] queries: (optional)
    """

    def __init__(self,
                 *,
                 type: str = None,
                 name: str = None,
                 id: str = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 queries: List['ResourceQuery'] = None) -> None:
        """
        Initialize a ResourceQueryRecord object.

        :param str type: (optional) Resource type (cluster, vsi, icd, vpc).
        :param str name: (optional) Resource query name.
        :param List[ResourceQuery] queries: (optional)
        """
        self.type = type
        self.name = name
        self.id = id
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.queries = queries

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryRecord':
        """Initialize a ResourceQueryRecord object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'queries' in _dict:
            args['queries'] = [ResourceQuery.from_dict(x) for x in _dict.get('queries')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryRecord object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'created_at') and getattr(self, 'created_at') is not None:
            _dict['created_at'] = datetime_to_string(getattr(self, 'created_at'))
        if hasattr(self, 'created_by') and getattr(self, 'created_by') is not None:
            _dict['created_by'] = getattr(self, 'created_by')
        if hasattr(self, 'updated_at') and getattr(self, 'updated_at') is not None:
            _dict['updated_at'] = datetime_to_string(getattr(self, 'updated_at'))
        if hasattr(self, 'updated_by') and getattr(self, 'updated_by') is not None:
            _dict['updated_by'] = getattr(self, 'updated_by')
        if hasattr(self, 'queries') and self.queries is not None:
            _dict['queries'] = [x.to_dict() for x in self.queries]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryRecord object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryRecord') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryRecord') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class TypeEnum(str, Enum):
        """
        Resource type (cluster, vsi, icd, vpc).
        """
        VSI = 'vsi'


class ResourceQueryRecordList():
    """
    List of Resource query records.

    :attr int total_count: (optional) Total number of records.
    :attr int limit: Number of records returned.
    :attr int offset: Skipped number of records.
    :attr List[ResourceQueryRecord] resource_queries: (optional) List of resource
          query records.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 total_count: int = None,
                 resource_queries: List['ResourceQueryRecord'] = None) -> None:
        """
        Initialize a ResourceQueryRecordList object.

        :param int limit: Number of records returned.
        :param int offset: Skipped number of records.
        :param int total_count: (optional) Total number of records.
        :param List[ResourceQueryRecord] resource_queries: (optional) List of
               resource query records.
        """
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.resource_queries = resource_queries

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryRecordList':
        """Initialize a ResourceQueryRecordList object from a json dictionary."""
        args = {}
        if 'total_count' in _dict:
            args['total_count'] = _dict.get('total_count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in ResourceQueryRecordList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in ResourceQueryRecordList JSON')
        if 'resource_queries' in _dict:
            args['resource_queries'] = [ResourceQueryRecord.from_dict(x) for x in _dict.get('resource_queries')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryRecordList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total_count') and self.total_count is not None:
            _dict['total_count'] = self.total_count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'resource_queries') and self.resource_queries is not None:
            _dict['resource_queries'] = [x.to_dict() for x in self.resource_queries]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryRecordList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryRecordList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryRecordList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQueryResponseRecord():
    """
    Describe resource query.

    :attr List[ResourceQueryResponseRecordResponse] response: (optional)
    """

    def __init__(self,
                 *,
                 response: List['ResourceQueryResponseRecordResponse'] = None) -> None:
        """
        Initialize a ResourceQueryResponseRecord object.

        :param List[ResourceQueryResponseRecordResponse] response: (optional)
        """
        self.response = response

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryResponseRecord':
        """Initialize a ResourceQueryResponseRecord object from a json dictionary."""
        args = {}
        if 'response' in _dict:
            args['response'] = [ResourceQueryResponseRecordResponse.from_dict(x) for x in _dict.get('response')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryResponseRecord object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'response') and self.response is not None:
            _dict['response'] = [x.to_dict() for x in self.response]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryResponseRecord object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryResponseRecord') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryResponseRecord') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQueryResponseRecordQueryOutput():
    """
    List of query output values.

    :attr str name: (optional) Name of the output param.
    :attr str value: (optional) value of the output param.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 value: str = None) -> None:
        """
        Initialize a ResourceQueryResponseRecordQueryOutput object.

        :param str name: (optional) Name of the output param.
        :param str value: (optional) value of the output param.
        """
        self.name = name
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryResponseRecordQueryOutput':
        """Initialize a ResourceQueryResponseRecordQueryOutput object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryResponseRecordQueryOutput object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryResponseRecordQueryOutput object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryResponseRecordQueryOutput') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryResponseRecordQueryOutput') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceQueryResponseRecordResponse():
    """
    ResourceQueryResponseRecordResponse.

    :attr str query_type: (optional) Type of the query(workspaces).
    :attr List[ResourceQueryParam] query_condition: (optional)
    :attr List[str] query_select: (optional) List of query selection parameters.
    :attr List[ResourceQueryResponseRecordQueryOutput] query_output: (optional)
    """

    def __init__(self,
                 *,
                 query_type: str = None,
                 query_condition: List['ResourceQueryParam'] = None,
                 query_select: List[str] = None,
                 query_output: List['ResourceQueryResponseRecordQueryOutput'] = None) -> None:
        """
        Initialize a ResourceQueryResponseRecordResponse object.

        :param str query_type: (optional) Type of the query(workspaces).
        :param List[ResourceQueryParam] query_condition: (optional)
        :param List[str] query_select: (optional) List of query selection
               parameters.
        :param List[ResourceQueryResponseRecordQueryOutput] query_output:
               (optional)
        """
        self.query_type = query_type
        self.query_condition = query_condition
        self.query_select = query_select
        self.query_output = query_output

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceQueryResponseRecordResponse':
        """Initialize a ResourceQueryResponseRecordResponse object from a json dictionary."""
        args = {}
        if 'query_type' in _dict:
            args['query_type'] = _dict.get('query_type')
        if 'query_condition' in _dict:
            args['query_condition'] = [ResourceQueryParam.from_dict(x) for x in _dict.get('query_condition')]
        if 'query_select' in _dict:
            args['query_select'] = _dict.get('query_select')
        if 'query_output' in _dict:
            args['query_output'] = [ResourceQueryResponseRecordQueryOutput.from_dict(x) for x in _dict.get('query_output')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceQueryResponseRecordResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'query_type') and self.query_type is not None:
            _dict['query_type'] = self.query_type
        if hasattr(self, 'query_condition') and self.query_condition is not None:
            _dict['query_condition'] = [x.to_dict() for x in self.query_condition]
        if hasattr(self, 'query_select') and self.query_select is not None:
            _dict['query_select'] = self.query_select
        if hasattr(self, 'query_output') and self.query_output is not None:
            _dict['query_output'] = [x.to_dict() for x in self.query_output]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceQueryResponseRecordResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceQueryResponseRecordResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceQueryResponseRecordResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class QueryTypeEnum(str, Enum):
        """
        Type of the query(workspaces).
        """
        WORKSPACES = 'workspaces'


class SchematicsLocations():
    """
    Information about the location.

    :attr str name: (optional) The name of the location.
    :attr str id: (optional) The ID of the location.
    :attr str country: (optional) The country where the location is located.
    :attr str geography: (optional) The geography that the location belongs to.
    :attr str geography_code: (optional) Geographical continent locations code
          having the data centres of IBM Cloud Schematics service.
    :attr str metro: (optional) The metro area that the location belongs to.
    :attr str multizone_metro: (optional) The multizone metro area that the location
          belongs to.
    :attr str kind: (optional) The kind of location.
    :attr List[str] paired_region: (optional) List of paired regions used by
          Schematics.
    :attr bool restricted: (optional) Restricted Region.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 id: str = None,
                 country: str = None,
                 geography: str = None,
                 geography_code: str = None,
                 metro: str = None,
                 multizone_metro: str = None,
                 kind: str = None,
                 paired_region: List[str] = None,
                 restricted: bool = None) -> None:
        """
        Initialize a SchematicsLocations object.

        :param str name: (optional) The name of the location.
        :param str id: (optional) The ID of the location.
        :param str country: (optional) The country where the location is located.
        :param str geography: (optional) The geography that the location belongs
               to.
        :param str geography_code: (optional) Geographical continent locations code
               having the data centres of IBM Cloud Schematics service.
        :param str metro: (optional) The metro area that the location belongs to.
        :param str multizone_metro: (optional) The multizone metro area that the
               location belongs to.
        :param str kind: (optional) The kind of location.
        :param List[str] paired_region: (optional) List of paired regions used by
               Schematics.
        :param bool restricted: (optional) Restricted Region.
        """
        self.name = name
        self.id = id
        self.country = country
        self.geography = geography
        self.geography_code = geography_code
        self.metro = metro
        self.multizone_metro = multizone_metro
        self.kind = kind
        self.paired_region = paired_region
        self.restricted = restricted

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SchematicsLocations':
        """Initialize a SchematicsLocations object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'country' in _dict:
            args['country'] = _dict.get('country')
        if 'geography' in _dict:
            args['geography'] = _dict.get('geography')
        if 'geography_code' in _dict:
            args['geography_code'] = _dict.get('geography_code')
        if 'metro' in _dict:
            args['metro'] = _dict.get('metro')
        if 'multizone_metro' in _dict:
            args['multizone_metro'] = _dict.get('multizone_metro')
        if 'kind' in _dict:
            args['kind'] = _dict.get('kind')
        if 'paired_region' in _dict:
            args['paired_region'] = _dict.get('paired_region')
        if 'restricted' in _dict:
            args['restricted'] = _dict.get('restricted')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SchematicsLocations object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'country') and self.country is not None:
            _dict['country'] = self.country
        if hasattr(self, 'geography') and self.geography is not None:
            _dict['geography'] = self.geography
        if hasattr(self, 'geography_code') and self.geography_code is not None:
            _dict['geography_code'] = self.geography_code
        if hasattr(self, 'metro') and self.metro is not None:
            _dict['metro'] = self.metro
        if hasattr(self, 'multizone_metro') and self.multizone_metro is not None:
            _dict['multizone_metro'] = self.multizone_metro
        if hasattr(self, 'kind') and self.kind is not None:
            _dict['kind'] = self.kind
        if hasattr(self, 'paired_region') and self.paired_region is not None:
            _dict['paired_region'] = self.paired_region
        if hasattr(self, 'restricted') and self.restricted is not None:
            _dict['restricted'] = self.restricted
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SchematicsLocations object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SchematicsLocations') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SchematicsLocations') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SchematicsLocationsList():
    """
    List of Locations details.

    :attr List[SchematicsLocationsLite] locations: (optional) List of Locations.
    """

    def __init__(self,
                 *,
                 locations: List['SchematicsLocationsLite'] = None) -> None:
        """
        Initialize a SchematicsLocationsList object.

        :param List[SchematicsLocationsLite] locations: (optional) List of
               Locations.
        """
        self.locations = locations

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SchematicsLocationsList':
        """Initialize a SchematicsLocationsList object from a json dictionary."""
        args = {}
        if 'locations' in _dict:
            args['locations'] = [SchematicsLocationsLite.from_dict(x) for x in _dict.get('locations')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SchematicsLocationsList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'locations') and self.locations is not None:
            _dict['locations'] = [x.to_dict() for x in self.locations]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SchematicsLocationsList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SchematicsLocationsList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SchematicsLocationsList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SchematicsLocationsLite():
    """
    individual location details.

    :attr str region: (optional) Geographical Region code having the data centres of
          IBM Cloud Schematics service.
    :attr str metro: (optional) Geographical city locations having the data centres
          of IBM Cloud Schematics service.
    :attr str geography_code: (optional) Geographical continent locations code
          having the data centres of IBM Cloud Schematics service.
    :attr str geography: (optional) Geographical continent locations having the data
          centres of IBM Cloud Schematics service.
    :attr str country: (optional) Country locations having the data centres of IBM
          Cloud Schematics service.
    :attr str kind: (optional) The kind of location.
    :attr List[str] paired_region: (optional) List of paired regions used by
          Schematics.
    :attr bool restricted: (optional) Restricted Region.
    """

    def __init__(self,
                 *,
                 region: str = None,
                 metro: str = None,
                 geography_code: str = None,
                 geography: str = None,
                 country: str = None,
                 kind: str = None,
                 paired_region: List[str] = None,
                 restricted: bool = None) -> None:
        """
        Initialize a SchematicsLocationsLite object.

        :param str region: (optional) Geographical Region code having the data
               centres of IBM Cloud Schematics service.
        :param str metro: (optional) Geographical city locations having the data
               centres of IBM Cloud Schematics service.
        :param str geography_code: (optional) Geographical continent locations code
               having the data centres of IBM Cloud Schematics service.
        :param str geography: (optional) Geographical continent locations having
               the data centres of IBM Cloud Schematics service.
        :param str country: (optional) Country locations having the data centres of
               IBM Cloud Schematics service.
        :param str kind: (optional) The kind of location.
        :param List[str] paired_region: (optional) List of paired regions used by
               Schematics.
        :param bool restricted: (optional) Restricted Region.
        """
        self.region = region
        self.metro = metro
        self.geography_code = geography_code
        self.geography = geography
        self.country = country
        self.kind = kind
        self.paired_region = paired_region
        self.restricted = restricted

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SchematicsLocationsLite':
        """Initialize a SchematicsLocationsLite object from a json dictionary."""
        args = {}
        if 'region' in _dict:
            args['region'] = _dict.get('region')
        if 'metro' in _dict:
            args['metro'] = _dict.get('metro')
        if 'geography_code' in _dict:
            args['geography_code'] = _dict.get('geography_code')
        if 'geography' in _dict:
            args['geography'] = _dict.get('geography')
        if 'country' in _dict:
            args['country'] = _dict.get('country')
        if 'kind' in _dict:
            args['kind'] = _dict.get('kind')
        if 'paired_region' in _dict:
            args['paired_region'] = _dict.get('paired_region')
        if 'restricted' in _dict:
            args['restricted'] = _dict.get('restricted')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SchematicsLocationsLite object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'region') and self.region is not None:
            _dict['region'] = self.region
        if hasattr(self, 'metro') and self.metro is not None:
            _dict['metro'] = self.metro
        if hasattr(self, 'geography_code') and self.geography_code is not None:
            _dict['geography_code'] = self.geography_code
        if hasattr(self, 'geography') and self.geography is not None:
            _dict['geography'] = self.geography
        if hasattr(self, 'country') and self.country is not None:
            _dict['country'] = self.country
        if hasattr(self, 'kind') and self.kind is not None:
            _dict['kind'] = self.kind
        if hasattr(self, 'paired_region') and self.paired_region is not None:
            _dict['paired_region'] = self.paired_region
        if hasattr(self, 'restricted') and self.restricted is not None:
            _dict['restricted'] = self.restricted
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SchematicsLocationsLite object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SchematicsLocationsLite') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SchematicsLocationsLite') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SharedTargetData():
    """
    Information about the Target used by the templates originating from the  IBM Cloud
    catalog offerings. This information is not relevant for workspace created using your
    own Terraform template.

    :attr str cluster_created_on: (optional) Cluster created on.
    :attr str cluster_id: (optional) The ID of the cluster where you want to
          provision the resources of all IBM Cloud catalog templates that are included in
          the catalog offering.
    :attr str cluster_name: (optional) The cluster name.
    :attr str cluster_type: (optional) The cluster type.
    :attr List[object] entitlement_keys: (optional) The entitlement key that you
          want to use to install IBM Cloud entitled software.
    :attr str namespace: (optional) The Kubernetes namespace or OpenShift project
          where the resources of all IBM Cloud catalog templates that are included in the
          catalog offering are deployed into.
    :attr str region: (optional) The IBM Cloud region that you want to use for the
          resources of all IBM Cloud catalog templates that are included in the catalog
          offering.
    :attr str resource_group_id: (optional) The ID of the resource group that you
          want to use for the resources of all IBM Cloud catalog templates that are
          included in the catalog offering.
    :attr int worker_count: (optional) The cluster worker count.
    :attr str worker_machine_type: (optional) The cluster worker type.
    """

    def __init__(self,
                 *,
                 cluster_created_on: str = None,
                 cluster_id: str = None,
                 cluster_name: str = None,
                 cluster_type: str = None,
                 entitlement_keys: List[object] = None,
                 namespace: str = None,
                 region: str = None,
                 resource_group_id: str = None,
                 worker_count: int = None,
                 worker_machine_type: str = None) -> None:
        """
        Initialize a SharedTargetData object.

        :param str cluster_created_on: (optional) Cluster created on.
        :param str cluster_id: (optional) The ID of the cluster where you want to
               provision the resources of all IBM Cloud catalog templates that are
               included in the catalog offering.
        :param str cluster_name: (optional) The cluster name.
        :param str cluster_type: (optional) The cluster type.
        :param List[object] entitlement_keys: (optional) The entitlement key that
               you want to use to install IBM Cloud entitled software.
        :param str namespace: (optional) The Kubernetes namespace or OpenShift
               project where the resources of all IBM Cloud catalog templates that are
               included in the catalog offering are deployed into.
        :param str region: (optional) The IBM Cloud region that you want to use for
               the resources of all IBM Cloud catalog templates that are included in the
               catalog offering.
        :param str resource_group_id: (optional) The ID of the resource group that
               you want to use for the resources of all IBM Cloud catalog templates that
               are included in the catalog offering.
        :param int worker_count: (optional) The cluster worker count.
        :param str worker_machine_type: (optional) The cluster worker type.
        """
        self.cluster_created_on = cluster_created_on
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.cluster_type = cluster_type
        self.entitlement_keys = entitlement_keys
        self.namespace = namespace
        self.region = region
        self.resource_group_id = resource_group_id
        self.worker_count = worker_count
        self.worker_machine_type = worker_machine_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SharedTargetData':
        """Initialize a SharedTargetData object from a json dictionary."""
        args = {}
        if 'cluster_created_on' in _dict:
            args['cluster_created_on'] = _dict.get('cluster_created_on')
        if 'cluster_id' in _dict:
            args['cluster_id'] = _dict.get('cluster_id')
        if 'cluster_name' in _dict:
            args['cluster_name'] = _dict.get('cluster_name')
        if 'cluster_type' in _dict:
            args['cluster_type'] = _dict.get('cluster_type')
        if 'entitlement_keys' in _dict:
            args['entitlement_keys'] = _dict.get('entitlement_keys')
        if 'namespace' in _dict:
            args['namespace'] = _dict.get('namespace')
        if 'region' in _dict:
            args['region'] = _dict.get('region')
        if 'resource_group_id' in _dict:
            args['resource_group_id'] = _dict.get('resource_group_id')
        if 'worker_count' in _dict:
            args['worker_count'] = _dict.get('worker_count')
        if 'worker_machine_type' in _dict:
            args['worker_machine_type'] = _dict.get('worker_machine_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SharedTargetData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cluster_created_on') and self.cluster_created_on is not None:
            _dict['cluster_created_on'] = self.cluster_created_on
        if hasattr(self, 'cluster_id') and self.cluster_id is not None:
            _dict['cluster_id'] = self.cluster_id
        if hasattr(self, 'cluster_name') and self.cluster_name is not None:
            _dict['cluster_name'] = self.cluster_name
        if hasattr(self, 'cluster_type') and self.cluster_type is not None:
            _dict['cluster_type'] = self.cluster_type
        if hasattr(self, 'entitlement_keys') and self.entitlement_keys is not None:
            _dict['entitlement_keys'] = self.entitlement_keys
        if hasattr(self, 'namespace') and self.namespace is not None:
            _dict['namespace'] = self.namespace
        if hasattr(self, 'region') and self.region is not None:
            _dict['region'] = self.region
        if hasattr(self, 'resource_group_id') and self.resource_group_id is not None:
            _dict['resource_group_id'] = self.resource_group_id
        if hasattr(self, 'worker_count') and self.worker_count is not None:
            _dict['worker_count'] = self.worker_count
        if hasattr(self, 'worker_machine_type') and self.worker_machine_type is not None:
            _dict['worker_machine_type'] = self.worker_machine_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SharedTargetData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SharedTargetData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SharedTargetData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SharedTargetDataResponse():
    """
    Information about the Target used by the templates originating from IBM Cloud catalog
    offerings. This information is not relevant when you create a workspace from your own
    Terraform template.

    :attr str cluster_id: (optional) The ID of the cluster where you want to
          provision the resources of all IBM Cloud catalog templates that are included in
          the catalog offering.
    :attr str cluster_name: (optional) Target cluster name.
    :attr List[object] entitlement_keys: (optional) The entitlement key that you
          want to use to install IBM Cloud entitled software.
    :attr str namespace: (optional) The Kubernetes namespace or OpenShift project
          where the resources of all IBM Cloud catalog templates that are included in the
          catalog offering are deployed into.
    :attr str region: (optional) The IBM Cloud region that you want to use for the
          resources of all IBM Cloud catalog templates that are included in the catalog
          offering.
    :attr str resource_group_id: (optional) The ID of the resource group that you
          want to use for the resources of all IBM Cloud catalog templates that are
          included in the catalog offering.
    """

    def __init__(self,
                 *,
                 cluster_id: str = None,
                 cluster_name: str = None,
                 entitlement_keys: List[object] = None,
                 namespace: str = None,
                 region: str = None,
                 resource_group_id: str = None) -> None:
        """
        Initialize a SharedTargetDataResponse object.

        :param str cluster_id: (optional) The ID of the cluster where you want to
               provision the resources of all IBM Cloud catalog templates that are
               included in the catalog offering.
        :param str cluster_name: (optional) Target cluster name.
        :param List[object] entitlement_keys: (optional) The entitlement key that
               you want to use to install IBM Cloud entitled software.
        :param str namespace: (optional) The Kubernetes namespace or OpenShift
               project where the resources of all IBM Cloud catalog templates that are
               included in the catalog offering are deployed into.
        :param str region: (optional) The IBM Cloud region that you want to use for
               the resources of all IBM Cloud catalog templates that are included in the
               catalog offering.
        :param str resource_group_id: (optional) The ID of the resource group that
               you want to use for the resources of all IBM Cloud catalog templates that
               are included in the catalog offering.
        """
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.entitlement_keys = entitlement_keys
        self.namespace = namespace
        self.region = region
        self.resource_group_id = resource_group_id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SharedTargetDataResponse':
        """Initialize a SharedTargetDataResponse object from a json dictionary."""
        args = {}
        if 'cluster_id' in _dict:
            args['cluster_id'] = _dict.get('cluster_id')
        if 'cluster_name' in _dict:
            args['cluster_name'] = _dict.get('cluster_name')
        if 'entitlement_keys' in _dict:
            args['entitlement_keys'] = _dict.get('entitlement_keys')
        if 'namespace' in _dict:
            args['namespace'] = _dict.get('namespace')
        if 'region' in _dict:
            args['region'] = _dict.get('region')
        if 'resource_group_id' in _dict:
            args['resource_group_id'] = _dict.get('resource_group_id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SharedTargetDataResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cluster_id') and self.cluster_id is not None:
            _dict['cluster_id'] = self.cluster_id
        if hasattr(self, 'cluster_name') and self.cluster_name is not None:
            _dict['cluster_name'] = self.cluster_name
        if hasattr(self, 'entitlement_keys') and self.entitlement_keys is not None:
            _dict['entitlement_keys'] = self.entitlement_keys
        if hasattr(self, 'namespace') and self.namespace is not None:
            _dict['namespace'] = self.namespace
        if hasattr(self, 'region') and self.region is not None:
            _dict['region'] = self.region
        if hasattr(self, 'resource_group_id') and self.resource_group_id is not None:
            _dict['resource_group_id'] = self.resource_group_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SharedTargetDataResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SharedTargetDataResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SharedTargetDataResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class StateStoreResponse():
    """
    Information about workspace runtime data.

    :attr str engine_name: (optional) The provisioning engine that was used to apply
          the Terraform template or IBM Cloud catalog software template.
    :attr str engine_version: (optional) The version of the provisioning engine that
          was used.
    :attr str id: (optional) The ID that was assigned to your Terraform template or
          IBM Cloud catalog software template.
    :attr str state_store_url: (optional) The URL where the Terraform statefile
          (`terraform.tfstate`) is stored. You can use the statefile to find an overview
          of IBM Cloud resources that were created by Schematics. Schematics uses the
          statefile as an inventory list to determine future create, update, or deletion
          jobs.
    """

    def __init__(self,
                 *,
                 engine_name: str = None,
                 engine_version: str = None,
                 id: str = None,
                 state_store_url: str = None) -> None:
        """
        Initialize a StateStoreResponse object.

        :param str engine_name: (optional) The provisioning engine that was used to
               apply the Terraform template or IBM Cloud catalog software template.
        :param str engine_version: (optional) The version of the provisioning
               engine that was used.
        :param str id: (optional) The ID that was assigned to your Terraform
               template or IBM Cloud catalog software template.
        :param str state_store_url: (optional) The URL where the Terraform
               statefile (`terraform.tfstate`) is stored. You can use the statefile to
               find an overview of IBM Cloud resources that were created by Schematics.
               Schematics uses the statefile as an inventory list to determine future
               create, update, or deletion jobs.
        """
        self.engine_name = engine_name
        self.engine_version = engine_version
        self.id = id
        self.state_store_url = state_store_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'StateStoreResponse':
        """Initialize a StateStoreResponse object from a json dictionary."""
        args = {}
        if 'engine_name' in _dict:
            args['engine_name'] = _dict.get('engine_name')
        if 'engine_version' in _dict:
            args['engine_version'] = _dict.get('engine_version')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'state_store_url' in _dict:
            args['state_store_url'] = _dict.get('state_store_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a StateStoreResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'engine_name') and self.engine_name is not None:
            _dict['engine_name'] = self.engine_name
        if hasattr(self, 'engine_version') and self.engine_version is not None:
            _dict['engine_version'] = self.engine_version
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'state_store_url') and self.state_store_url is not None:
            _dict['state_store_url'] = self.state_store_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this StateStoreResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'StateStoreResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'StateStoreResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class StateStoreResponseList():
    """
    Information about the Terraform statefile URL.

    :attr List[StateStoreResponse] runtime_data: (optional) Information about
          workspace runtime data.
    """

    def __init__(self,
                 *,
                 runtime_data: List['StateStoreResponse'] = None) -> None:
        """
        Initialize a StateStoreResponseList object.

        :param List[StateStoreResponse] runtime_data: (optional) Information about
               workspace runtime data.
        """
        self.runtime_data = runtime_data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'StateStoreResponseList':
        """Initialize a StateStoreResponseList object from a json dictionary."""
        args = {}
        if 'runtime_data' in _dict:
            args['runtime_data'] = [StateStoreResponse.from_dict(x) for x in _dict.get('runtime_data')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a StateStoreResponseList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'runtime_data') and self.runtime_data is not None:
            _dict['runtime_data'] = [x.to_dict() for x in self.runtime_data]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this StateStoreResponseList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'StateStoreResponseList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'StateStoreResponseList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SystemLock():
    """
    System lock status.

    :attr bool sys_locked: (optional) Is the automation locked by a Schematic job ?.
    :attr str sys_locked_by: (optional) Name of the User who performed the job, that
          lead to the locking of the automation.
    :attr datetime sys_locked_at: (optional) When the User performed the job that
          lead to locking of the automation ?.
    """

    def __init__(self,
                 *,
                 sys_locked: bool = None,
                 sys_locked_by: str = None,
                 sys_locked_at: datetime = None) -> None:
        """
        Initialize a SystemLock object.

        :param bool sys_locked: (optional) Is the automation locked by a Schematic
               job ?.
        :param str sys_locked_by: (optional) Name of the User who performed the
               job, that lead to the locking of the automation.
        :param datetime sys_locked_at: (optional) When the User performed the job
               that lead to locking of the automation ?.
        """
        self.sys_locked = sys_locked
        self.sys_locked_by = sys_locked_by
        self.sys_locked_at = sys_locked_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SystemLock':
        """Initialize a SystemLock object from a json dictionary."""
        args = {}
        if 'sys_locked' in _dict:
            args['sys_locked'] = _dict.get('sys_locked')
        if 'sys_locked_by' in _dict:
            args['sys_locked_by'] = _dict.get('sys_locked_by')
        if 'sys_locked_at' in _dict:
            args['sys_locked_at'] = string_to_datetime(_dict.get('sys_locked_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SystemLock object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'sys_locked') and self.sys_locked is not None:
            _dict['sys_locked'] = self.sys_locked
        if hasattr(self, 'sys_locked_by') and self.sys_locked_by is not None:
            _dict['sys_locked_by'] = self.sys_locked_by
        if hasattr(self, 'sys_locked_at') and self.sys_locked_at is not None:
            _dict['sys_locked_at'] = datetime_to_string(self.sys_locked_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SystemLock object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SystemLock') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SystemLock') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateMetaDataResponse():
    """
    Template metadata response.

    :attr str type: (optional) Template type (terraform, ansible, helm, cloudpak,
          bash script).
    :attr List[VariableData] variables: List of variables and its metadata.
    """

    def __init__(self,
                 variables: List['VariableData'],
                 *,
                 type: str = None) -> None:
        """
        Initialize a TemplateMetaDataResponse object.

        :param List[VariableData] variables: List of variables and its metadata.
        :param str type: (optional) Template type (terraform, ansible, helm,
               cloudpak, bash script).
        """
        self.type = type
        self.variables = variables

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateMetaDataResponse':
        """Initialize a TemplateMetaDataResponse object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'variables' in _dict:
            args['variables'] = [VariableData.from_dict(x) for x in _dict.get('variables')]
        else:
            raise ValueError('Required property \'variables\' not present in TemplateMetaDataResponse JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateMetaDataResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'variables') and self.variables is not None:
            _dict['variables'] = [x.to_dict() for x in self.variables]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateMetaDataResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateMetaDataResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateMetaDataResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateReadme():
    """
    The `README.md` file for the template used by the workspace.

    :attr str readme: (optional) The `README.md` file for the template used by the
          workspace.
    """

    def __init__(self,
                 *,
                 readme: str = None) -> None:
        """
        Initialize a TemplateReadme object.

        :param str readme: (optional) The `README.md` file for the template used by
               the workspace.
        """
        self.readme = readme

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateReadme':
        """Initialize a TemplateReadme object from a json dictionary."""
        args = {}
        if 'readme' in _dict:
            args['readme'] = _dict.get('readme')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateReadme object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'readme') and self.readme is not None:
            _dict['readme'] = self.readme
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateReadme object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateReadme') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateReadme') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRepoRequest():
    """
    Input variables for the Template repoository, while creating a workspace.

    :attr str branch: (optional) The repository branch.
    :attr str release: (optional) The repository release.
    :attr str repo_sha_value: (optional) The repository SHA value.
    :attr str repo_url: (optional) The repository URL.
    :attr str url: (optional) The source URL.
    """

    def __init__(self,
                 *,
                 branch: str = None,
                 release: str = None,
                 repo_sha_value: str = None,
                 repo_url: str = None,
                 url: str = None) -> None:
        """
        Initialize a TemplateRepoRequest object.

        :param str branch: (optional) The repository branch.
        :param str release: (optional) The repository release.
        :param str repo_sha_value: (optional) The repository SHA value.
        :param str repo_url: (optional) The repository URL.
        :param str url: (optional) The source URL.
        """
        self.branch = branch
        self.release = release
        self.repo_sha_value = repo_sha_value
        self.repo_url = repo_url
        self.url = url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRepoRequest':
        """Initialize a TemplateRepoRequest object from a json dictionary."""
        args = {}
        if 'branch' in _dict:
            args['branch'] = _dict.get('branch')
        if 'release' in _dict:
            args['release'] = _dict.get('release')
        if 'repo_sha_value' in _dict:
            args['repo_sha_value'] = _dict.get('repo_sha_value')
        if 'repo_url' in _dict:
            args['repo_url'] = _dict.get('repo_url')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRepoRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'branch') and self.branch is not None:
            _dict['branch'] = self.branch
        if hasattr(self, 'release') and self.release is not None:
            _dict['release'] = self.release
        if hasattr(self, 'repo_sha_value') and self.repo_sha_value is not None:
            _dict['repo_sha_value'] = self.repo_sha_value
        if hasattr(self, 'repo_url') and self.repo_url is not None:
            _dict['repo_url'] = self.repo_url
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRepoRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRepoRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRepoRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRepoResponse():
    """
    Information about the Template repository used by the workspace.

    :attr str branch: (optional) The repository branch.
    :attr str full_url: (optional) Full repository URL.
    :attr bool has_uploadedgitrepotar: (optional) Has uploaded Git repository tar.
    :attr str release: (optional) The repository release.
    :attr str repo_sha_value: (optional) The repository SHA value.
    :attr str repo_url: (optional) The repository URL.
    :attr str url: (optional) The source URL.
    """

    def __init__(self,
                 *,
                 branch: str = None,
                 full_url: str = None,
                 has_uploadedgitrepotar: bool = None,
                 release: str = None,
                 repo_sha_value: str = None,
                 repo_url: str = None,
                 url: str = None) -> None:
        """
        Initialize a TemplateRepoResponse object.

        :param str branch: (optional) The repository branch.
        :param str full_url: (optional) Full repository URL.
        :param bool has_uploadedgitrepotar: (optional) Has uploaded Git repository
               tar.
        :param str release: (optional) The repository release.
        :param str repo_sha_value: (optional) The repository SHA value.
        :param str repo_url: (optional) The repository URL.
        :param str url: (optional) The source URL.
        """
        self.branch = branch
        self.full_url = full_url
        self.has_uploadedgitrepotar = has_uploadedgitrepotar
        self.release = release
        self.repo_sha_value = repo_sha_value
        self.repo_url = repo_url
        self.url = url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRepoResponse':
        """Initialize a TemplateRepoResponse object from a json dictionary."""
        args = {}
        if 'branch' in _dict:
            args['branch'] = _dict.get('branch')
        if 'full_url' in _dict:
            args['full_url'] = _dict.get('full_url')
        if 'has_uploadedgitrepotar' in _dict:
            args['has_uploadedgitrepotar'] = _dict.get('has_uploadedgitrepotar')
        if 'release' in _dict:
            args['release'] = _dict.get('release')
        if 'repo_sha_value' in _dict:
            args['repo_sha_value'] = _dict.get('repo_sha_value')
        if 'repo_url' in _dict:
            args['repo_url'] = _dict.get('repo_url')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRepoResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'branch') and self.branch is not None:
            _dict['branch'] = self.branch
        if hasattr(self, 'full_url') and self.full_url is not None:
            _dict['full_url'] = self.full_url
        if hasattr(self, 'has_uploadedgitrepotar') and self.has_uploadedgitrepotar is not None:
            _dict['has_uploadedgitrepotar'] = self.has_uploadedgitrepotar
        if hasattr(self, 'release') and self.release is not None:
            _dict['release'] = self.release
        if hasattr(self, 'repo_sha_value') and self.repo_sha_value is not None:
            _dict['repo_sha_value'] = self.repo_sha_value
        if hasattr(self, 'repo_url') and self.repo_url is not None:
            _dict['repo_url'] = self.repo_url
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRepoResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRepoResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRepoResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRepoTarUploadResponse():
    """
    TemplateRepoTarUploadResponse -.

    :attr str file_value: (optional) Tar file value.
    :attr bool has_received_file: (optional) Has received tar file?.
    :attr str id: (optional) Template ID.
    """

    def __init__(self,
                 *,
                 file_value: str = None,
                 has_received_file: bool = None,
                 id: str = None) -> None:
        """
        Initialize a TemplateRepoTarUploadResponse object.

        :param str file_value: (optional) Tar file value.
        :param bool has_received_file: (optional) Has received tar file?.
        :param str id: (optional) Template ID.
        """
        self.file_value = file_value
        self.has_received_file = has_received_file
        self.id = id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRepoTarUploadResponse':
        """Initialize a TemplateRepoTarUploadResponse object from a json dictionary."""
        args = {}
        if 'file_value' in _dict:
            args['file_value'] = _dict.get('file_value')
        if 'has_received_file' in _dict:
            args['has_received_file'] = _dict.get('has_received_file')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRepoTarUploadResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'file_value') and self.file_value is not None:
            _dict['file_value'] = self.file_value
        if hasattr(self, 'has_received_file') and self.has_received_file is not None:
            _dict['has_received_file'] = self.has_received_file
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRepoTarUploadResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRepoTarUploadResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRepoTarUploadResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRepoUpdateRequest():
    """
    Input to update the template repository data.

    :attr str branch: (optional) The repository branch.
    :attr str release: (optional) The repository release.
    :attr str repo_sha_value: (optional) The repository SHA value.
    :attr str repo_url: (optional) The repository URL.
    :attr str url: (optional) The source URL.
    """

    def __init__(self,
                 *,
                 branch: str = None,
                 release: str = None,
                 repo_sha_value: str = None,
                 repo_url: str = None,
                 url: str = None) -> None:
        """
        Initialize a TemplateRepoUpdateRequest object.

        :param str branch: (optional) The repository branch.
        :param str release: (optional) The repository release.
        :param str repo_sha_value: (optional) The repository SHA value.
        :param str repo_url: (optional) The repository URL.
        :param str url: (optional) The source URL.
        """
        self.branch = branch
        self.release = release
        self.repo_sha_value = repo_sha_value
        self.repo_url = repo_url
        self.url = url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRepoUpdateRequest':
        """Initialize a TemplateRepoUpdateRequest object from a json dictionary."""
        args = {}
        if 'branch' in _dict:
            args['branch'] = _dict.get('branch')
        if 'release' in _dict:
            args['release'] = _dict.get('release')
        if 'repo_sha_value' in _dict:
            args['repo_sha_value'] = _dict.get('repo_sha_value')
        if 'repo_url' in _dict:
            args['repo_url'] = _dict.get('repo_url')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRepoUpdateRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'branch') and self.branch is not None:
            _dict['branch'] = self.branch
        if hasattr(self, 'release') and self.release is not None:
            _dict['release'] = self.release
        if hasattr(self, 'repo_sha_value') and self.repo_sha_value is not None:
            _dict['repo_sha_value'] = self.repo_sha_value
        if hasattr(self, 'repo_url') and self.repo_url is not None:
            _dict['repo_url'] = self.repo_url
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRepoUpdateRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRepoUpdateRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRepoUpdateRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateResources():
    """
    Information about the resources provisioned by the Terraform template.

    :attr str folder: (optional) The subfolder in GitHub or GitLab where your
          Terraform templates are stored.  If your template is stored in the root
          directory, `.` is returned.
    :attr str id: (optional) The ID that was assigned to your Terraform template or
          IBM Cloud catalog software template.
    :attr List[object] null_resources: (optional) List of null resources.
    :attr List[object] related_resources: (optional) Information about the IBM Cloud
          resources that are associated with your workspace.
    :attr List[object] resources: (optional) Information about the IBM Cloud
          resources that are associated with your workspace. **Note** The
          `resource_tainted` flag marks `true` when an instance is times out after few
          hours, if your resource provisioning takes longer duration. When you rerun the
          apply plan, based on the `resource_taint` flag result the provisioning continues
          from the state where the provisioning has stopped.
    :attr int resources_count: (optional) Number of resources.
    :attr str template_type: (optional) The Terraform version that was used to apply
          your template.
    """

    def __init__(self,
                 *,
                 folder: str = None,
                 id: str = None,
                 null_resources: List[object] = None,
                 related_resources: List[object] = None,
                 resources: List[object] = None,
                 resources_count: int = None,
                 template_type: str = None) -> None:
        """
        Initialize a TemplateResources object.

        :param str folder: (optional) The subfolder in GitHub or GitLab where your
               Terraform templates are stored.  If your template is stored in the root
               directory, `.` is returned.
        :param str id: (optional) The ID that was assigned to your Terraform
               template or IBM Cloud catalog software template.
        :param List[object] null_resources: (optional) List of null resources.
        :param List[object] related_resources: (optional) Information about the IBM
               Cloud resources that are associated with your workspace.
        :param List[object] resources: (optional) Information about the IBM Cloud
               resources that are associated with your workspace. **Note** The
               `resource_tainted` flag marks `true` when an instance is times out after
               few hours, if your resource provisioning takes longer duration. When you
               rerun the apply plan, based on the `resource_taint` flag result the
               provisioning continues from the state where the provisioning has stopped.
        :param int resources_count: (optional) Number of resources.
        :param str template_type: (optional) The Terraform version that was used to
               apply your template.
        """
        self.folder = folder
        self.id = id
        self.null_resources = null_resources
        self.related_resources = related_resources
        self.resources = resources
        self.resources_count = resources_count
        self.template_type = template_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateResources':
        """Initialize a TemplateResources object from a json dictionary."""
        args = {}
        if 'folder' in _dict:
            args['folder'] = _dict.get('folder')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'null_resources' in _dict:
            args['null_resources'] = _dict.get('null_resources')
        if 'related_resources' in _dict:
            args['related_resources'] = _dict.get('related_resources')
        if 'resources' in _dict:
            args['resources'] = _dict.get('resources')
        if 'resources_count' in _dict:
            args['resources_count'] = _dict.get('resources_count')
        if 'template_type' in _dict:
            args['template_type'] = _dict.get('template_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'folder') and self.folder is not None:
            _dict['folder'] = self.folder
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'null_resources') and self.null_resources is not None:
            _dict['null_resources'] = self.null_resources
        if hasattr(self, 'related_resources') and self.related_resources is not None:
            _dict['related_resources'] = self.related_resources
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = self.resources
        if hasattr(self, 'resources_count') and self.resources_count is not None:
            _dict['resources_count'] = self.resources_count
        if hasattr(self, 'template_type') and self.template_type is not None:
            _dict['template_type'] = self.template_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateRunTimeDataResponse():
    """
    Information about the provisioning engine, state file, and runtime logs.

    :attr str engine_cmd: (optional) The command that was used to apply the
          Terraform template or IBM Cloud catalog software template.
    :attr str engine_name: (optional) The provisioning engine that was used to apply
          the Terraform template or IBM Cloud catalog software template.
    :attr str engine_version: (optional) The version of the provisioning engine that
          was used.
    :attr str id: (optional) The ID that was assigned to your Terraform template or
          IBM Cloud catalog software template.
    :attr str log_store_url: (optional) The URL to access the logs that were created
          during the creation, update, or deletion of your IBM Cloud resources.
    :attr List[object] output_values: (optional) List of Output values.
    :attr List[List[object]] resources: (optional) List of resources.
    :attr str state_store_url: (optional) The URL where the Terraform statefile
          (`terraform.tfstate`) is stored. You can use the statefile to find an overview
          of IBM Cloud resources that were created by Schematics. Schematics uses the
          statefile as an inventory list to determine future create, update, or deletion
          jobs.
    """

    def __init__(self,
                 *,
                 engine_cmd: str = None,
                 engine_name: str = None,
                 engine_version: str = None,
                 id: str = None,
                 log_store_url: str = None,
                 output_values: List[object] = None,
                 resources: List[List[object]] = None,
                 state_store_url: str = None) -> None:
        """
        Initialize a TemplateRunTimeDataResponse object.

        :param str engine_cmd: (optional) The command that was used to apply the
               Terraform template or IBM Cloud catalog software template.
        :param str engine_name: (optional) The provisioning engine that was used to
               apply the Terraform template or IBM Cloud catalog software template.
        :param str engine_version: (optional) The version of the provisioning
               engine that was used.
        :param str id: (optional) The ID that was assigned to your Terraform
               template or IBM Cloud catalog software template.
        :param str log_store_url: (optional) The URL to access the logs that were
               created during the creation, update, or deletion of your IBM Cloud
               resources.
        :param List[object] output_values: (optional) List of Output values.
        :param List[List[object]] resources: (optional) List of resources.
        :param str state_store_url: (optional) The URL where the Terraform
               statefile (`terraform.tfstate`) is stored. You can use the statefile to
               find an overview of IBM Cloud resources that were created by Schematics.
               Schematics uses the statefile as an inventory list to determine future
               create, update, or deletion jobs.
        """
        self.engine_cmd = engine_cmd
        self.engine_name = engine_name
        self.engine_version = engine_version
        self.id = id
        self.log_store_url = log_store_url
        self.output_values = output_values
        self.resources = resources
        self.state_store_url = state_store_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateRunTimeDataResponse':
        """Initialize a TemplateRunTimeDataResponse object from a json dictionary."""
        args = {}
        if 'engine_cmd' in _dict:
            args['engine_cmd'] = _dict.get('engine_cmd')
        if 'engine_name' in _dict:
            args['engine_name'] = _dict.get('engine_name')
        if 'engine_version' in _dict:
            args['engine_version'] = _dict.get('engine_version')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'log_store_url' in _dict:
            args['log_store_url'] = _dict.get('log_store_url')
        if 'output_values' in _dict:
            args['output_values'] = _dict.get('output_values')
        if 'resources' in _dict:
            args['resources'] = _dict.get('resources')
        if 'state_store_url' in _dict:
            args['state_store_url'] = _dict.get('state_store_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateRunTimeDataResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'engine_cmd') and self.engine_cmd is not None:
            _dict['engine_cmd'] = self.engine_cmd
        if hasattr(self, 'engine_name') and self.engine_name is not None:
            _dict['engine_name'] = self.engine_name
        if hasattr(self, 'engine_version') and self.engine_version is not None:
            _dict['engine_version'] = self.engine_version
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'log_store_url') and self.log_store_url is not None:
            _dict['log_store_url'] = self.log_store_url
        if hasattr(self, 'output_values') and self.output_values is not None:
            _dict['output_values'] = self.output_values
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = self.resources
        if hasattr(self, 'state_store_url') and self.state_store_url is not None:
            _dict['state_store_url'] = self.state_store_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateRunTimeDataResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateRunTimeDataResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateRunTimeDataResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateSourceDataRequest():
    """
    Input parameters to define input variables for your Terraform template.

    :attr List[object] env_values: (optional) A list of environment variables that
          you want to apply during the execution of a bash script or Terraform job. This
          field must be provided as a list of key-value pairs, for example,
          **TF_LOG=debug**. Each entry will be a map with one entry where `key is the
          environment variable name and value is value`. You can define environment
          variables for IBM Cloud catalog offerings that are provisioned by using a bash
          script. See [example to use special environment
          variable](https://cloud.ibm.com/docs/schematics?topic=schematics-set-parallelism#parallelism-example)
           that are supported by Schematics.
    :attr str folder: (optional) The subfolder in your GitHub or GitLab repository
          where your Terraform template is stored.
    :attr bool compact: (optional) True, to use the files from the specified folder
          & subfolder in your GitHub or GitLab repository and ignore the other folders in
          the repository.
    :attr str init_state_file: (optional) The content of an existing Terraform
          statefile that you want to import in to your workspace. To get the content of a
          Terraform statefile for a specific Terraform template in an existing workspace,
          run `ibmcloud terraform state pull --id <workspace_id> --template
          <template_id>`.
    :attr str type: (optional) The Terraform version that you want to use to run
          your Terraform code. Enter `terraform_v0.12` to use Terraform version 0.12, and
          `terraform_v0.11` to use Terraform version 0.11. The Terraform config files are
          run with Terraform version 0.11. This is a required variable. Make sure that
          your Terraform config files are compatible with the Terraform version that you
          select.
    :attr str uninstall_script_name: (optional) Uninstall script name.
    :attr str values: (optional) A list of variable values that you want to apply
          during the Helm chart installation. The list must be provided in JSON format,
          such as `"autoscaling: enabled: true minReplicas: 2"`. The values that you
          define here override the default Helm chart values. This field is supported only
          for IBM Cloud catalog offerings that are provisioned by using the Terraform Helm
          provider.
    :attr List[object] values_metadata: (optional) List of values metadata.
    :attr List[WorkspaceVariableRequest] variablestore: (optional) VariablesRequest
          -.
    """

    def __init__(self,
                 *,
                 env_values: List[object] = None,
                 folder: str = None,
                 compact: bool = None,
                 init_state_file: str = None,
                 type: str = None,
                 uninstall_script_name: str = None,
                 values: str = None,
                 values_metadata: List[object] = None,
                 variablestore: List['WorkspaceVariableRequest'] = None) -> None:
        """
        Initialize a TemplateSourceDataRequest object.

        :param List[object] env_values: (optional) A list of environment variables
               that you want to apply during the execution of a bash script or Terraform
               job. This field must be provided as a list of key-value pairs, for example,
               **TF_LOG=debug**. Each entry will be a map with one entry where `key is the
               environment variable name and value is value`. You can define environment
               variables for IBM Cloud catalog offerings that are provisioned by using a
               bash script. See [example to use special environment
               variable](https://cloud.ibm.com/docs/schematics?topic=schematics-set-parallelism#parallelism-example)
                that are supported by Schematics.
        :param str folder: (optional) The subfolder in your GitHub or GitLab
               repository where your Terraform template is stored.
        :param bool compact: (optional) True, to use the files from the specified
               folder & subfolder in your GitHub or GitLab repository and ignore the other
               folders in the repository.
        :param str init_state_file: (optional) The content of an existing Terraform
               statefile that you want to import in to your workspace. To get the content
               of a Terraform statefile for a specific Terraform template in an existing
               workspace, run `ibmcloud terraform state pull --id <workspace_id>
               --template <template_id>`.
        :param str type: (optional) The Terraform version that you want to use to
               run your Terraform code. Enter `terraform_v0.12` to use Terraform version
               0.12, and `terraform_v0.11` to use Terraform version 0.11. The Terraform
               config files are run with Terraform version 0.11. This is a required
               variable. Make sure that your Terraform config files are compatible with
               the Terraform version that you select.
        :param str uninstall_script_name: (optional) Uninstall script name.
        :param str values: (optional) A list of variable values that you want to
               apply during the Helm chart installation. The list must be provided in JSON
               format, such as `"autoscaling: enabled: true minReplicas: 2"`. The values
               that you define here override the default Helm chart values. This field is
               supported only for IBM Cloud catalog offerings that are provisioned by
               using the Terraform Helm provider.
        :param List[object] values_metadata: (optional) List of values metadata.
        :param List[WorkspaceVariableRequest] variablestore: (optional)
               VariablesRequest -.
        """
        self.env_values = env_values
        self.folder = folder
        self.compact = compact
        self.init_state_file = init_state_file
        self.type = type
        self.uninstall_script_name = uninstall_script_name
        self.values = values
        self.values_metadata = values_metadata
        self.variablestore = variablestore

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateSourceDataRequest':
        """Initialize a TemplateSourceDataRequest object from a json dictionary."""
        args = {}
        if 'env_values' in _dict:
            args['env_values'] = _dict.get('env_values')
        if 'folder' in _dict:
            args['folder'] = _dict.get('folder')
        if 'compact' in _dict:
            args['compact'] = _dict.get('compact')
        if 'init_state_file' in _dict:
            args['init_state_file'] = _dict.get('init_state_file')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'uninstall_script_name' in _dict:
            args['uninstall_script_name'] = _dict.get('uninstall_script_name')
        if 'values' in _dict:
            args['values'] = _dict.get('values')
        if 'values_metadata' in _dict:
            args['values_metadata'] = _dict.get('values_metadata')
        if 'variablestore' in _dict:
            args['variablestore'] = [WorkspaceVariableRequest.from_dict(x) for x in _dict.get('variablestore')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateSourceDataRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'env_values') and self.env_values is not None:
            _dict['env_values'] = self.env_values
        if hasattr(self, 'folder') and self.folder is not None:
            _dict['folder'] = self.folder
        if hasattr(self, 'compact') and self.compact is not None:
            _dict['compact'] = self.compact
        if hasattr(self, 'init_state_file') and self.init_state_file is not None:
            _dict['init_state_file'] = self.init_state_file
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'uninstall_script_name') and self.uninstall_script_name is not None:
            _dict['uninstall_script_name'] = self.uninstall_script_name
        if hasattr(self, 'values') and self.values is not None:
            _dict['values'] = self.values
        if hasattr(self, 'values_metadata') and self.values_metadata is not None:
            _dict['values_metadata'] = self.values_metadata
        if hasattr(self, 'variablestore') and self.variablestore is not None:
            _dict['variablestore'] = [x.to_dict() for x in self.variablestore]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateSourceDataRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateSourceDataRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateSourceDataRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateSourceDataResponse():
    """
    Information about the input variables that are used in the template.

    :attr List[EnvVariableResponse] env_values: (optional) List of environment
          values.
    :attr str folder: (optional) The subfolder in your GitHub or GitLab repository
          where your Terraform template is stored. If your template is stored in the root
          directory, `.` is returned.
    :attr bool compact: (optional) True, to use the files from the specified folder
          & subfolder in your GitHub or GitLab repository and ignore the other folders in
          the repository.
    :attr bool has_githubtoken: (optional) Has github token.
    :attr str id: (optional) The ID that was assigned to your Terraform template or
          IBM Cloud catalog software template.
    :attr str type: (optional) The Terraform version that was used to run your
          Terraform code.
    :attr str uninstall_script_name: (optional) Uninstall script name.
    :attr str values: (optional) A list of variable values that you want to apply
          during the Helm chart installation. The list must be provided in JSON format,
          such as `"autoscaling: enabled: true minReplicas: 2"`. The values that you
          define here override the default Helm chart values. This field is supported only
          for IBM Cloud catalog offerings that are provisioned by using the Terraform Helm
          provider.
    :attr List[object] values_metadata: (optional) A list of input variables that
          are associated with the workspace.
    :attr str values_url: (optional) The API endpoint to access the input variables
          that you defined for your template.
    :attr List[WorkspaceVariableResponse] variablestore: (optional) Information
          about the input variables that your template uses.
    """

    def __init__(self,
                 *,
                 env_values: List['EnvVariableResponse'] = None,
                 folder: str = None,
                 compact: bool = None,
                 has_githubtoken: bool = None,
                 id: str = None,
                 type: str = None,
                 uninstall_script_name: str = None,
                 values: str = None,
                 values_metadata: List[object] = None,
                 values_url: str = None,
                 variablestore: List['WorkspaceVariableResponse'] = None) -> None:
        """
        Initialize a TemplateSourceDataResponse object.

        :param List[EnvVariableResponse] env_values: (optional) List of environment
               values.
        :param str folder: (optional) The subfolder in your GitHub or GitLab
               repository where your Terraform template is stored. If your template is
               stored in the root directory, `.` is returned.
        :param bool compact: (optional) True, to use the files from the specified
               folder & subfolder in your GitHub or GitLab repository and ignore the other
               folders in the repository.
        :param bool has_githubtoken: (optional) Has github token.
        :param str id: (optional) The ID that was assigned to your Terraform
               template or IBM Cloud catalog software template.
        :param str type: (optional) The Terraform version that was used to run your
               Terraform code.
        :param str uninstall_script_name: (optional) Uninstall script name.
        :param str values: (optional) A list of variable values that you want to
               apply during the Helm chart installation. The list must be provided in JSON
               format, such as `"autoscaling: enabled: true minReplicas: 2"`. The values
               that you define here override the default Helm chart values. This field is
               supported only for IBM Cloud catalog offerings that are provisioned by
               using the Terraform Helm provider.
        :param List[object] values_metadata: (optional) A list of input variables
               that are associated with the workspace.
        :param str values_url: (optional) The API endpoint to access the input
               variables that you defined for your template.
        :param List[WorkspaceVariableResponse] variablestore: (optional)
               Information about the input variables that your template uses.
        """
        self.env_values = env_values
        self.folder = folder
        self.compact = compact
        self.has_githubtoken = has_githubtoken
        self.id = id
        self.type = type
        self.uninstall_script_name = uninstall_script_name
        self.values = values
        self.values_metadata = values_metadata
        self.values_url = values_url
        self.variablestore = variablestore

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateSourceDataResponse':
        """Initialize a TemplateSourceDataResponse object from a json dictionary."""
        args = {}
        if 'env_values' in _dict:
            args['env_values'] = [EnvVariableResponse.from_dict(x) for x in _dict.get('env_values')]
        if 'folder' in _dict:
            args['folder'] = _dict.get('folder')
        if 'compact' in _dict:
            args['compact'] = _dict.get('compact')
        if 'has_githubtoken' in _dict:
            args['has_githubtoken'] = _dict.get('has_githubtoken')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'uninstall_script_name' in _dict:
            args['uninstall_script_name'] = _dict.get('uninstall_script_name')
        if 'values' in _dict:
            args['values'] = _dict.get('values')
        if 'values_metadata' in _dict:
            args['values_metadata'] = _dict.get('values_metadata')
        if 'values_url' in _dict:
            args['values_url'] = _dict.get('values_url')
        if 'variablestore' in _dict:
            args['variablestore'] = [WorkspaceVariableResponse.from_dict(x) for x in _dict.get('variablestore')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateSourceDataResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'env_values') and self.env_values is not None:
            _dict['env_values'] = [x.to_dict() for x in self.env_values]
        if hasattr(self, 'folder') and self.folder is not None:
            _dict['folder'] = self.folder
        if hasattr(self, 'compact') and self.compact is not None:
            _dict['compact'] = self.compact
        if hasattr(self, 'has_githubtoken') and self.has_githubtoken is not None:
            _dict['has_githubtoken'] = self.has_githubtoken
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'uninstall_script_name') and self.uninstall_script_name is not None:
            _dict['uninstall_script_name'] = self.uninstall_script_name
        if hasattr(self, 'values') and self.values is not None:
            _dict['values'] = self.values
        if hasattr(self, 'values_metadata') and self.values_metadata is not None:
            _dict['values_metadata'] = self.values_metadata
        if hasattr(self, 'values_url') and self.values_url is not None:
            _dict['values_url'] = self.values_url
        if hasattr(self, 'variablestore') and self.variablestore is not None:
            _dict['variablestore'] = [x.to_dict() for x in self.variablestore]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateSourceDataResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateSourceDataResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateSourceDataResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TemplateValues():
    """
    Information about the input variables that are declared in the template that your
    workspace points to.

    :attr List[object] values_metadata: (optional)
    """

    def __init__(self,
                 *,
                 values_metadata: List[object] = None) -> None:
        """
        Initialize a TemplateValues object.

        :param List[object] values_metadata: (optional)
        """
        self.values_metadata = values_metadata

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TemplateValues':
        """Initialize a TemplateValues object from a json dictionary."""
        args = {}
        if 'values_metadata' in _dict:
            args['values_metadata'] = _dict.get('values_metadata')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TemplateValues object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'values_metadata') and self.values_metadata is not None:
            _dict['values_metadata'] = self.values_metadata
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TemplateValues object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TemplateValues') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TemplateValues') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class TerraformCommand():
    """
    Inputs for running a Terraform command on the workspace.

    :attr str command: (optional) You must provide the command to execute. Supported
          commands are `show`,`taint`, `untaint`, `state`, `import`, `output`.
    :attr str command_params: (optional) The required address parameters for the
          command name. You can send the option flag and address parameter in the payload.
          **Syntax ** "command_params": "<option>=<flag>", "<address>". **Example **
          "command_params": "-allow-missing=true", "-lock=true",
          "data.template_file.test".
    :attr str command_name: (optional) The optional name for the command block.
    :attr str command_desc: (optional) The optional text to describe the command
          block.
    :attr str command_on_error: (optional) Instruction to continue or break in case
          of error.
    :attr str command_depends_on: (optional) Dependency on previous commands.
    :attr str command_status: (optional) Displays the command executed status,
          either `success` or `failure`.
    """

    def __init__(self,
                 *,
                 command: str = None,
                 command_params: str = None,
                 command_name: str = None,
                 command_desc: str = None,
                 command_on_error: str = None,
                 command_depends_on: str = None,
                 command_status: str = None) -> None:
        """
        Initialize a TerraformCommand object.

        :param str command: (optional) You must provide the command to execute.
               Supported commands are `show`,`taint`, `untaint`, `state`, `import`,
               `output`.
        :param str command_params: (optional) The required address parameters for
               the command name. You can send the option flag and address parameter in the
               payload. **Syntax ** "command_params": "<option>=<flag>", "<address>".
               **Example ** "command_params": "-allow-missing=true", "-lock=true",
               "data.template_file.test".
        :param str command_name: (optional) The optional name for the command
               block.
        :param str command_desc: (optional) The optional text to describe the
               command block.
        :param str command_on_error: (optional) Instruction to continue or break in
               case of error.
        :param str command_depends_on: (optional) Dependency on previous commands.
        :param str command_status: (optional) Displays the command executed status,
               either `success` or `failure`.
        """
        self.command = command
        self.command_params = command_params
        self.command_name = command_name
        self.command_desc = command_desc
        self.command_on_error = command_on_error
        self.command_depends_on = command_depends_on
        self.command_status = command_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TerraformCommand':
        """Initialize a TerraformCommand object from a json dictionary."""
        args = {}
        if 'command' in _dict:
            args['command'] = _dict.get('command')
        if 'command_params' in _dict:
            args['command_params'] = _dict.get('command_params')
        if 'command_name' in _dict:
            args['command_name'] = _dict.get('command_name')
        if 'command_desc' in _dict:
            args['command_desc'] = _dict.get('command_desc')
        if 'command_on_error' in _dict:
            args['command_on_error'] = _dict.get('command_on_error')
        if 'command_depends_on' in _dict:
            args['command_depends_on'] = _dict.get('command_depends_on')
        if 'command_status' in _dict:
            args['command_status'] = _dict.get('command_status')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TerraformCommand object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'command') and self.command is not None:
            _dict['command'] = self.command
        if hasattr(self, 'command_params') and self.command_params is not None:
            _dict['command_params'] = self.command_params
        if hasattr(self, 'command_name') and self.command_name is not None:
            _dict['command_name'] = self.command_name
        if hasattr(self, 'command_desc') and self.command_desc is not None:
            _dict['command_desc'] = self.command_desc
        if hasattr(self, 'command_on_error') and self.command_on_error is not None:
            _dict['command_on_error'] = self.command_on_error
        if hasattr(self, 'command_depends_on') and self.command_depends_on is not None:
            _dict['command_depends_on'] = self.command_depends_on
        if hasattr(self, 'command_status') and self.command_status is not None:
            _dict['command_status'] = self.command_status
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TerraformCommand object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TerraformCommand') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TerraformCommand') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UserState():
    """
    User defined status of the Schematics object.

    :attr str state: (optional) User-defined states
            * `draft` Object can be modified; can be used by Jobs run by the author,
          during execution
            * `live` Object can be modified; can be used by Jobs during execution
            * `locked` Object cannot be modified; can be used by Jobs during execution
            * `disable` Object can be modified. cannot be used by Jobs during execution.
    :attr str set_by: (optional) Name of the User who set the state of the Object.
    :attr datetime set_at: (optional) When the User who set the state of the Object.
    """

    def __init__(self,
                 *,
                 state: str = None,
                 set_by: str = None,
                 set_at: datetime = None) -> None:
        """
        Initialize a UserState object.

        :param str state: (optional) User-defined states
                 * `draft` Object can be modified; can be used by Jobs run by the author,
               during execution
                 * `live` Object can be modified; can be used by Jobs during execution
                 * `locked` Object cannot be modified; can be used by Jobs during
               execution
                 * `disable` Object can be modified. cannot be used by Jobs during
               execution.
        :param str set_by: (optional) Name of the User who set the state of the
               Object.
        :param datetime set_at: (optional) When the User who set the state of the
               Object.
        """
        self.state = state
        self.set_by = set_by
        self.set_at = set_at

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UserState':
        """Initialize a UserState object from a json dictionary."""
        args = {}
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        if 'set_by' in _dict:
            args['set_by'] = _dict.get('set_by')
        if 'set_at' in _dict:
            args['set_at'] = string_to_datetime(_dict.get('set_at'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UserState object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state
        if hasattr(self, 'set_by') and self.set_by is not None:
            _dict['set_by'] = self.set_by
        if hasattr(self, 'set_at') and self.set_at is not None:
            _dict['set_at'] = datetime_to_string(self.set_at)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UserState object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UserState') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UserState') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StateEnum(str, Enum):
        """
        User-defined states
          * `draft` Object can be modified; can be used by Jobs run by the author, during
        execution
          * `live` Object can be modified; can be used by Jobs during execution
          * `locked` Object cannot be modified; can be used by Jobs during execution
          * `disable` Object can be modified. cannot be used by Jobs during execution.
        """
        DRAFT = 'draft'
        LIVE = 'live'
        LOCKED = 'locked'
        DISABLE = 'disable'


class UserValues():
    """
    UserValues -.

    :attr List[object] env_values: (optional) A list of environment variables that
          you want to apply during the execution of a bash script or Terraform job. This
          field must be provided as a list of key-value pairs, for example,
          **TF_LOG=debug**. Each entry will be a map with one entry where `key is the
          environment variable name and value is value`. You can define environment
          variables for IBM Cloud catalog offerings that are provisioned by using a bash
          script. See [example to use special environment
          variable](https://cloud.ibm.com/docs/schematics?topic=schematics-set-parallelism#parallelism-example)
           that are supported by Schematics.
    :attr str values: (optional) User values.
    :attr List[WorkspaceVariableResponse] variablestore: (optional) Information
          about the input variables that your template uses.
    """

    def __init__(self,
                 *,
                 env_values: List[object] = None,
                 values: str = None,
                 variablestore: List['WorkspaceVariableResponse'] = None) -> None:
        """
        Initialize a UserValues object.

        :param List[object] env_values: (optional) A list of environment variables
               that you want to apply during the execution of a bash script or Terraform
               job. This field must be provided as a list of key-value pairs, for example,
               **TF_LOG=debug**. Each entry will be a map with one entry where `key is the
               environment variable name and value is value`. You can define environment
               variables for IBM Cloud catalog offerings that are provisioned by using a
               bash script. See [example to use special environment
               variable](https://cloud.ibm.com/docs/schematics?topic=schematics-set-parallelism#parallelism-example)
                that are supported by Schematics.
        :param str values: (optional) User values.
        :param List[WorkspaceVariableResponse] variablestore: (optional)
               Information about the input variables that your template uses.
        """
        self.env_values = env_values
        self.values = values
        self.variablestore = variablestore

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UserValues':
        """Initialize a UserValues object from a json dictionary."""
        args = {}
        if 'env_values' in _dict:
            args['env_values'] = _dict.get('env_values')
        if 'values' in _dict:
            args['values'] = _dict.get('values')
        if 'variablestore' in _dict:
            args['variablestore'] = [WorkspaceVariableResponse.from_dict(x) for x in _dict.get('variablestore')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UserValues object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'env_values') and self.env_values is not None:
            _dict['env_values'] = self.env_values
        if hasattr(self, 'values') and self.values is not None:
            _dict['values'] = self.values
        if hasattr(self, 'variablestore') and self.variablestore is not None:
            _dict['variablestore'] = [x.to_dict() for x in self.variablestore]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UserValues object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UserValues') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UserValues') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class VariableData():
    """
    User editable variable data & system generated reference to value.

    :attr str name: (optional) Name of the variable.
    :attr str value: (optional) Value for the variable or reference to the value.
    :attr VariableMetadata metadata: (optional) User editable metadata for the
          variables.
    :attr str link: (optional) Reference link to the variable value By default the
          expression will point to self.value.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 value: str = None,
                 metadata: 'VariableMetadata' = None,
                 link: str = None) -> None:
        """
        Initialize a VariableData object.

        :param str name: (optional) Name of the variable.
        :param str value: (optional) Value for the variable or reference to the
               value.
        :param VariableMetadata metadata: (optional) User editable metadata for the
               variables.
        """
        self.name = name
        self.value = value
        self.metadata = metadata
        self.link = link

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'VariableData':
        """Initialize a VariableData object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        if 'metadata' in _dict:
            args['metadata'] = VariableMetadata.from_dict(_dict.get('metadata'))
        if 'link' in _dict:
            args['link'] = _dict.get('link')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a VariableData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        if hasattr(self, 'metadata') and self.metadata is not None:
            _dict['metadata'] = self.metadata.to_dict()
        if hasattr(self, 'link') and getattr(self, 'link') is not None:
            _dict['link'] = getattr(self, 'link')
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this VariableData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'VariableData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VariableData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class VariableMetadata():
    """
    User editable metadata for the variables.

    :attr str type: (optional) Type of the variable.
    :attr List[str] aliases: (optional) List of aliases for the variable name.
    :attr str description: (optional) Description of the meta data.
    :attr str default_value: (optional) Default value for the variable, if the
          override value is not specified.
    :attr bool secure: (optional) Is the variable secure or sensitive ?.
    :attr bool immutable: (optional) Is the variable readonly ?.
    :attr bool hidden: (optional) If true, the variable will not be displayed on UI
          or CLI.
    :attr List[str] options: (optional) List of possible values for this variable.
          If type is integer or date, then the array of string will be  converted to array
          of integers or date during runtime.
    :attr int min_value: (optional) Minimum value of the variable. Applicable for
          integer type.
    :attr int max_value: (optional) Maximum value of the variable. Applicable for
          integer type.
    :attr int min_length: (optional) Minimum length of the variable value.
          Applicable for string type.
    :attr int max_length: (optional) Maximum length of the variable value.
          Applicable for string type.
    :attr str matches: (optional) Regex for the variable value.
    :attr int position: (optional) Relative position of this variable in a list.
    :attr str group_by: (optional) Display name of the group this variable belongs
          to.
    :attr str source: (optional) Source of this meta-data.
    """

    def __init__(self,
                 *,
                 type: str = None,
                 aliases: List[str] = None,
                 description: str = None,
                 default_value: str = None,
                 secure: bool = None,
                 immutable: bool = None,
                 hidden: bool = None,
                 options: List[str] = None,
                 min_value: int = None,
                 max_value: int = None,
                 min_length: int = None,
                 max_length: int = None,
                 matches: str = None,
                 position: int = None,
                 group_by: str = None,
                 source: str = None) -> None:
        """
        Initialize a VariableMetadata object.

        :param str type: (optional) Type of the variable.
        :param List[str] aliases: (optional) List of aliases for the variable name.
        :param str description: (optional) Description of the meta data.
        :param str default_value: (optional) Default value for the variable, if the
               override value is not specified.
        :param bool secure: (optional) Is the variable secure or sensitive ?.
        :param bool immutable: (optional) Is the variable readonly ?.
        :param bool hidden: (optional) If true, the variable will not be displayed
               on UI or CLI.
        :param List[str] options: (optional) List of possible values for this
               variable.  If type is integer or date, then the array of string will be
               converted to array of integers or date during runtime.
        :param int min_value: (optional) Minimum value of the variable. Applicable
               for integer type.
        :param int max_value: (optional) Maximum value of the variable. Applicable
               for integer type.
        :param int min_length: (optional) Minimum length of the variable value.
               Applicable for string type.
        :param int max_length: (optional) Maximum length of the variable value.
               Applicable for string type.
        :param str matches: (optional) Regex for the variable value.
        :param int position: (optional) Relative position of this variable in a
               list.
        :param str group_by: (optional) Display name of the group this variable
               belongs to.
        :param str source: (optional) Source of this meta-data.
        """
        self.type = type
        self.aliases = aliases
        self.description = description
        self.default_value = default_value
        self.secure = secure
        self.immutable = immutable
        self.hidden = hidden
        self.options = options
        self.min_value = min_value
        self.max_value = max_value
        self.min_length = min_length
        self.max_length = max_length
        self.matches = matches
        self.position = position
        self.group_by = group_by
        self.source = source

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'VariableMetadata':
        """Initialize a VariableMetadata object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'aliases' in _dict:
            args['aliases'] = _dict.get('aliases')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'default_value' in _dict:
            args['default_value'] = _dict.get('default_value')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'immutable' in _dict:
            args['immutable'] = _dict.get('immutable')
        if 'hidden' in _dict:
            args['hidden'] = _dict.get('hidden')
        if 'options' in _dict:
            args['options'] = _dict.get('options')
        if 'min_value' in _dict:
            args['min_value'] = _dict.get('min_value')
        if 'max_value' in _dict:
            args['max_value'] = _dict.get('max_value')
        if 'min_length' in _dict:
            args['min_length'] = _dict.get('min_length')
        if 'max_length' in _dict:
            args['max_length'] = _dict.get('max_length')
        if 'matches' in _dict:
            args['matches'] = _dict.get('matches')
        if 'position' in _dict:
            args['position'] = _dict.get('position')
        if 'group_by' in _dict:
            args['group_by'] = _dict.get('group_by')
        if 'source' in _dict:
            args['source'] = _dict.get('source')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a VariableMetadata object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'aliases') and self.aliases is not None:
            _dict['aliases'] = self.aliases
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'default_value') and self.default_value is not None:
            _dict['default_value'] = self.default_value
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'immutable') and self.immutable is not None:
            _dict['immutable'] = self.immutable
        if hasattr(self, 'hidden') and self.hidden is not None:
            _dict['hidden'] = self.hidden
        if hasattr(self, 'options') and self.options is not None:
            _dict['options'] = self.options
        if hasattr(self, 'min_value') and self.min_value is not None:
            _dict['min_value'] = self.min_value
        if hasattr(self, 'max_value') and self.max_value is not None:
            _dict['max_value'] = self.max_value
        if hasattr(self, 'min_length') and self.min_length is not None:
            _dict['min_length'] = self.min_length
        if hasattr(self, 'max_length') and self.max_length is not None:
            _dict['max_length'] = self.max_length
        if hasattr(self, 'matches') and self.matches is not None:
            _dict['matches'] = self.matches
        if hasattr(self, 'position') and self.position is not None:
            _dict['position'] = self.position
        if hasattr(self, 'group_by') and self.group_by is not None:
            _dict['group_by'] = self.group_by
        if hasattr(self, 'source') and self.source is not None:
            _dict['source'] = self.source
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this VariableMetadata object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'VariableMetadata') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VariableMetadata') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class TypeEnum(str, Enum):
        """
        Type of the variable.
        """
        BOOLEAN = 'boolean'
        STRING = 'string'
        INTEGER = 'integer'
        DATE = 'date'
        ARRAY = 'array'
        LIST = 'list'
        MAP = 'map'
        COMPLEX = 'complex'


class VersionResponse():
    """
    Successful response when you retrieve detailed information about the IBM Cloud
    Schematics API.

    :attr str builddate: (optional) The date when the API version was built.
    :attr str buildno: (optional) The build number that the API is based on.
    :attr str commitsha: (optional) The SHA value for the Git commit that represents
          the latest version of the API.
    :attr str helm_provider_version: (optional) The Terraform Helm provider version
          that is used when you install Helm charts with Schematics.
    :attr str helm_version: (optional) The Helm version that is used when you
          install Helm charts with Schematics.
    :attr object supported_template_types: (optional) Supported template types.
    :attr str terraform_provider_version: (optional) The version of the IBM Cloud
          Terraform provider plug-in that is used when you apply Terraform templates with
          Schematics.
    :attr str terraform_version: (optional) The Terraform version that is used when
          you apply Terraform templates with Schematics.
    """

    def __init__(self,
                 *,
                 builddate: str = None,
                 buildno: str = None,
                 commitsha: str = None,
                 helm_provider_version: str = None,
                 helm_version: str = None,
                 supported_template_types: object = None,
                 terraform_provider_version: str = None,
                 terraform_version: str = None) -> None:
        """
        Initialize a VersionResponse object.

        :param str builddate: (optional) The date when the API version was built.
        :param str buildno: (optional) The build number that the API is based on.
        :param str commitsha: (optional) The SHA value for the Git commit that
               represents the latest version of the API.
        :param str helm_provider_version: (optional) The Terraform Helm provider
               version that is used when you install Helm charts with Schematics.
        :param str helm_version: (optional) The Helm version that is used when you
               install Helm charts with Schematics.
        :param object supported_template_types: (optional) Supported template
               types.
        :param str terraform_provider_version: (optional) The version of the IBM
               Cloud Terraform provider plug-in that is used when you apply Terraform
               templates with Schematics.
        :param str terraform_version: (optional) The Terraform version that is used
               when you apply Terraform templates with Schematics.
        """
        self.builddate = builddate
        self.buildno = buildno
        self.commitsha = commitsha
        self.helm_provider_version = helm_provider_version
        self.helm_version = helm_version
        self.supported_template_types = supported_template_types
        self.terraform_provider_version = terraform_provider_version
        self.terraform_version = terraform_version

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'VersionResponse':
        """Initialize a VersionResponse object from a json dictionary."""
        args = {}
        if 'builddate' in _dict:
            args['builddate'] = _dict.get('builddate')
        if 'buildno' in _dict:
            args['buildno'] = _dict.get('buildno')
        if 'commitsha' in _dict:
            args['commitsha'] = _dict.get('commitsha')
        if 'helm_provider_version' in _dict:
            args['helm_provider_version'] = _dict.get('helm_provider_version')
        if 'helm_version' in _dict:
            args['helm_version'] = _dict.get('helm_version')
        if 'supported_template_types' in _dict:
            args['supported_template_types'] = _dict.get('supported_template_types')
        if 'terraform_provider_version' in _dict:
            args['terraform_provider_version'] = _dict.get('terraform_provider_version')
        if 'terraform_version' in _dict:
            args['terraform_version'] = _dict.get('terraform_version')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a VersionResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'builddate') and self.builddate is not None:
            _dict['builddate'] = self.builddate
        if hasattr(self, 'buildno') and self.buildno is not None:
            _dict['buildno'] = self.buildno
        if hasattr(self, 'commitsha') and self.commitsha is not None:
            _dict['commitsha'] = self.commitsha
        if hasattr(self, 'helm_provider_version') and self.helm_provider_version is not None:
            _dict['helm_provider_version'] = self.helm_provider_version
        if hasattr(self, 'helm_version') and self.helm_version is not None:
            _dict['helm_version'] = self.helm_version
        if hasattr(self, 'supported_template_types') and self.supported_template_types is not None:
            _dict['supported_template_types'] = self.supported_template_types
        if hasattr(self, 'terraform_provider_version') and self.terraform_provider_version is not None:
            _dict['terraform_provider_version'] = self.terraform_provider_version
        if hasattr(self, 'terraform_version') and self.terraform_version is not None:
            _dict['terraform_version'] = self.terraform_version
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this VersionResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'VersionResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VersionResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivities():
    """
    List of workspace jobs.

    :attr List[WorkspaceActivity] actions: (optional) List of workspace jobs.
    :attr str workspace_id: (optional) The ID of the workspace.
    :attr str workspace_name: (optional) The name of the workspace.
    """

    def __init__(self,
                 *,
                 actions: List['WorkspaceActivity'] = None,
                 workspace_id: str = None,
                 workspace_name: str = None) -> None:
        """
        Initialize a WorkspaceActivities object.

        :param List[WorkspaceActivity] actions: (optional) List of workspace jobs.
        :param str workspace_id: (optional) The ID of the workspace.
        :param str workspace_name: (optional) The name of the workspace.
        """
        self.actions = actions
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivities':
        """Initialize a WorkspaceActivities object from a json dictionary."""
        args = {}
        if 'actions' in _dict:
            args['actions'] = [WorkspaceActivity.from_dict(x) for x in _dict.get('actions')]
        if 'workspace_id' in _dict:
            args['workspace_id'] = _dict.get('workspace_id')
        if 'workspace_name' in _dict:
            args['workspace_name'] = _dict.get('workspace_name')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivities object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'actions') and self.actions is not None:
            _dict['actions'] = [x.to_dict() for x in self.actions]
        if hasattr(self, 'workspace_id') and self.workspace_id is not None:
            _dict['workspace_id'] = self.workspace_id
        if hasattr(self, 'workspace_name') and self.workspace_name is not None:
            _dict['workspace_name'] = self.workspace_name
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivities object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivities') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivities') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivity():
    """
    Information about the workspace jobs.

    :attr str action_id: (optional) The ID of the activity or job.  You can use the
          ID to retrieve the logs for that job by using the `GET
          /v1/workspaces/{id}/actions/{action_id}/logs` API.
    :attr List[str] message: (optional) Information about the success or failure of
          your job,  including a success or error code and the timestamp when the job
          succeeded or failed.
    :attr str name: (optional) The type of actovoty or job that ran against your
          workspace.
           * **APPLY**: The apply job was created when you used the `PUT
          /v1/workspaces/{id}/apply` API to apply a Terraform template in IBM Cloud.
           * **DESTROY**: The destroy job was created when you used the `DELETE
          /v1/workspaces/{id}/destroy` API to remove all resources that are associated
          with your workspace.
           * **PLAN**: The plan job was created when you used the `POST
          /v1/workspaces/{id}/plan` API to create a Terraform execution plan.
    :attr datetime performed_at: (optional) The timestamp when the job was
          initiated.
    :attr str performed_by: (optional) The user ID who initiated the job.
    :attr str status: (optional) The status of your activity or job. To retrieve the
          URL to your job logs, use the GET /v1/workspaces/{id}/actions/{action_id}/logs
          API.
          * **COMPLETED**: The job completed successfully.
          * **CREATED**: The job was created, but the provisioning, modification, or
          removal of IBM Cloud resources has not started yet.
          * **FAILED**: An error occurred during the plan, apply, or destroy job. Use the
          job ID to retrieve the URL to the log files for your job.
          * **IN PROGRESS**: The job is in progress. You can use the log_url to access the
          logs.
    :attr List[WorkspaceActivityTemplate] templates: (optional) List of template
          activities.
    """

    def __init__(self,
                 *,
                 action_id: str = None,
                 message: List[str] = None,
                 name: str = None,
                 performed_at: datetime = None,
                 performed_by: str = None,
                 status: str = None,
                 templates: List['WorkspaceActivityTemplate'] = None) -> None:
        """
        Initialize a WorkspaceActivity object.

        :param str action_id: (optional) The ID of the activity or job.  You can
               use the ID to retrieve the logs for that job by using the `GET
               /v1/workspaces/{id}/actions/{action_id}/logs` API.
        :param List[str] message: (optional) Information about the success or
               failure of your job,  including a success or error code and the timestamp
               when the job succeeded or failed.
        :param str name: (optional) The type of actovoty or job that ran against
               your workspace.
                * **APPLY**: The apply job was created when you used the `PUT
               /v1/workspaces/{id}/apply` API to apply a Terraform template in IBM Cloud.
                * **DESTROY**: The destroy job was created when you used the `DELETE
               /v1/workspaces/{id}/destroy` API to remove all resources that are
               associated with your workspace.
                * **PLAN**: The plan job was created when you used the `POST
               /v1/workspaces/{id}/plan` API to create a Terraform execution plan.
        :param datetime performed_at: (optional) The timestamp when the job was
               initiated.
        :param str performed_by: (optional) The user ID who initiated the job.
        :param str status: (optional) The status of your activity or job. To
               retrieve the URL to your job logs, use the GET
               /v1/workspaces/{id}/actions/{action_id}/logs API.
               * **COMPLETED**: The job completed successfully.
               * **CREATED**: The job was created, but the provisioning, modification, or
               removal of IBM Cloud resources has not started yet.
               * **FAILED**: An error occurred during the plan, apply, or destroy job. Use
               the job ID to retrieve the URL to the log files for your job.
               * **IN PROGRESS**: The job is in progress. You can use the log_url to
               access the logs.
        :param List[WorkspaceActivityTemplate] templates: (optional) List of
               template activities.
        """
        self.action_id = action_id
        self.message = message
        self.name = name
        self.performed_at = performed_at
        self.performed_by = performed_by
        self.status = status
        self.templates = templates

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivity':
        """Initialize a WorkspaceActivity object from a json dictionary."""
        args = {}
        if 'action_id' in _dict:
            args['action_id'] = _dict.get('action_id')
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'performed_at' in _dict:
            args['performed_at'] = string_to_datetime(_dict.get('performed_at'))
        if 'performed_by' in _dict:
            args['performed_by'] = _dict.get('performed_by')
        if 'status' in _dict:
            args['status'] = _dict.get('status')
        if 'templates' in _dict:
            args['templates'] = [WorkspaceActivityTemplate.from_dict(x) for x in _dict.get('templates')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivity object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_id') and self.action_id is not None:
            _dict['action_id'] = self.action_id
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'performed_at') and self.performed_at is not None:
            _dict['performed_at'] = datetime_to_string(self.performed_at)
        if hasattr(self, 'performed_by') and self.performed_by is not None:
            _dict['performed_by'] = self.performed_by
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'templates') and self.templates is not None:
            _dict['templates'] = [x.to_dict() for x in self.templates]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivity object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivity') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivity') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityApplyResult():
    """
    Response after successfully initiating a request to `apply` the Terraform template in
    IBM Cloud.

    :attr str activityid: (optional) The ID of the activity or job that was created
          when you initiated a request to `apply` a Terraform template.  You can use the
          ID to retrieve log file by using the `GET
          /v1/workspaces/{id}/actions/{action_id}/logs` API.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityApplyResult object.

        :param str activityid: (optional) The ID of the activity or job that was
               created when you initiated a request to `apply` a Terraform template.  You
               can use the ID to retrieve log file by using the `GET
               /v1/workspaces/{id}/actions/{action_id}/logs` API.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityApplyResult':
        """Initialize a WorkspaceActivityApplyResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityApplyResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityApplyResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityApplyResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityApplyResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityCommandResult():
    """
    Response after successfully initiating a request to run a workspace command on the
    stack of resources provisioned using Terraform.

    :attr str activityid: (optional) The ID of the job that was created when you
          initiated a request to `apply` a Terraform template.  You can use the ID to
          retrieve log file by using the `GET
          /v1/workspaces/{id}/actions/{action_id}/logs` API.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityCommandResult object.

        :param str activityid: (optional) The ID of the job that was created when
               you initiated a request to `apply` a Terraform template.  You can use the
               ID to retrieve log file by using the `GET
               /v1/workspaces/{id}/actions/{action_id}/logs` API.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityCommandResult':
        """Initialize a WorkspaceActivityCommandResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityCommandResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityCommandResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityCommandResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityCommandResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityDestroyResult():
    """
    Response after successfully initiating a request to `destroy` the stack of resources
    provisioned using Terraform.

    :attr str activityid: (optional) The ID of the activity or job that was created
          when you initiated a request to `destroy` a Terraform template.  You can use the
          ID to retrieve log file by using the `GET
          /v1/workspaces/{id}/actions/{action_id}/logs` API.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityDestroyResult object.

        :param str activityid: (optional) The ID of the activity or job that was
               created when you initiated a request to `destroy` a Terraform template.
               You can use the ID to retrieve log file by using the `GET
               /v1/workspaces/{id}/actions/{action_id}/logs` API.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityDestroyResult':
        """Initialize a WorkspaceActivityDestroyResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityDestroyResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityDestroyResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityDestroyResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityDestroyResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityLogs():
    """
    Workspace job logs for all the templates in the workspace.

    :attr str action_id: (optional) The ID of the activity or job that ran against
          your workspace.
    :attr str name: (optional) The type of actovoty or job that ran against your
          workspace.
           * **APPLY**: The apply job was created when you used the `PUT
          /v1/workspaces/{id}/apply` API to apply a Terraform template in IBM Cloud.
           * **DESTROY**: The destroy job was created when you used the `DELETE
          /v1/workspaces/{id}/destroy` API to remove all resources that are associated
          with your workspace.
           * **PLAN**: The plan job was created when you used the `POST
          /v1/workspaces/{id}/plan` API to create a Terraform execution plan.
    :attr List[WorkspaceActivityTemplateLogs] templates: (optional) List of
          templates in the workspace.
    """

    def __init__(self,
                 *,
                 action_id: str = None,
                 name: str = None,
                 templates: List['WorkspaceActivityTemplateLogs'] = None) -> None:
        """
        Initialize a WorkspaceActivityLogs object.

        :param str action_id: (optional) The ID of the activity or job that ran
               against your workspace.
        :param str name: (optional) The type of actovoty or job that ran against
               your workspace.
                * **APPLY**: The apply job was created when you used the `PUT
               /v1/workspaces/{id}/apply` API to apply a Terraform template in IBM Cloud.
                * **DESTROY**: The destroy job was created when you used the `DELETE
               /v1/workspaces/{id}/destroy` API to remove all resources that are
               associated with your workspace.
                * **PLAN**: The plan job was created when you used the `POST
               /v1/workspaces/{id}/plan` API to create a Terraform execution plan.
        :param List[WorkspaceActivityTemplateLogs] templates: (optional) List of
               templates in the workspace.
        """
        self.action_id = action_id
        self.name = name
        self.templates = templates

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityLogs':
        """Initialize a WorkspaceActivityLogs object from a json dictionary."""
        args = {}
        if 'action_id' in _dict:
            args['action_id'] = _dict.get('action_id')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'templates' in _dict:
            args['templates'] = [WorkspaceActivityTemplateLogs.from_dict(x) for x in _dict.get('templates')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityLogs object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'action_id') and self.action_id is not None:
            _dict['action_id'] = self.action_id
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'templates') and self.templates is not None:
            _dict['templates'] = [x.to_dict() for x in self.templates]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityLogs object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityLogs') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityLogs') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityOptionsTemplate():
    """
    Workspace job options template.

    :attr List[str] target: (optional) A list of Terraform resources to target.
    :attr List[str] tf_vars: (optional) Terraform variables for the workspace job
          options.
    """

    def __init__(self,
                 *,
                 target: List[str] = None,
                 tf_vars: List[str] = None) -> None:
        """
        Initialize a WorkspaceActivityOptionsTemplate object.

        :param List[str] target: (optional) A list of Terraform resources to
               target.
        :param List[str] tf_vars: (optional) Terraform variables for the workspace
               job options.
        """
        self.target = target
        self.tf_vars = tf_vars

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityOptionsTemplate':
        """Initialize a WorkspaceActivityOptionsTemplate object from a json dictionary."""
        args = {}
        if 'target' in _dict:
            args['target'] = _dict.get('target')
        if 'tf_vars' in _dict:
            args['tf_vars'] = _dict.get('tf_vars')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityOptionsTemplate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'target') and self.target is not None:
            _dict['target'] = self.target
        if hasattr(self, 'tf_vars') and self.tf_vars is not None:
            _dict['tf_vars'] = self.tf_vars
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityOptionsTemplate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityOptionsTemplate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityOptionsTemplate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityPlanResult():
    """
    Response after successfully initiating a request to `plan` the Terraform template in
    IBM Cloud.

    :attr str activityid: (optional) The ID of the activity or job that was created
          when you initiated a request to `plan` a Terraform template.  You can use the ID
          to retrieve log file by using the `GET
          /v1/workspaces/{id}/actions/{action_id}/logs` API.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityPlanResult object.

        :param str activityid: (optional) The ID of the activity or job that was
               created when you initiated a request to `plan` a Terraform template.  You
               can use the ID to retrieve log file by using the `GET
               /v1/workspaces/{id}/actions/{action_id}/logs` API.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityPlanResult':
        """Initialize a WorkspaceActivityPlanResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityPlanResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityPlanResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityPlanResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityPlanResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityRefreshResult():
    """
    Response after successfully initiating a request to `refresh` the Terraform template
    in IBM Cloud.

    :attr str activityid: (optional) The ID of the activity or job that was created
          for your workspace `refresh` activity or job.  You can use the ID to retrieve
          the log file by using the `GET /v1/workspaces/{id}/actions/{action_id}/logs`
          API.
    """

    def __init__(self,
                 *,
                 activityid: str = None) -> None:
        """
        Initialize a WorkspaceActivityRefreshResult object.

        :param str activityid: (optional) The ID of the activity or job that was
               created for your workspace `refresh` activity or job.  You can use the ID
               to retrieve the log file by using the `GET
               /v1/workspaces/{id}/actions/{action_id}/logs` API.
        """
        self.activityid = activityid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityRefreshResult':
        """Initialize a WorkspaceActivityRefreshResult object from a json dictionary."""
        args = {}
        if 'activityid' in _dict:
            args['activityid'] = _dict.get('activityid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityRefreshResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activityid') and self.activityid is not None:
            _dict['activityid'] = self.activityid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityRefreshResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityRefreshResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityRefreshResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityTemplate():
    """
    Information about the template in the workspace.

    :attr datetime end_time: (optional) End time for the job.
    :attr LogSummary log_summary: (optional) Summary information extracted from the
          job logs.
    :attr str log_url: (optional) Log URL.
    :attr str message: (optional) Message.
    :attr datetime start_time: (optional) Job start time.
    :attr str status: (optional) The status of your activity or job. To retrieve the
          URL to your job logs, use the GET /v1/workspaces/{id}/actions/{action_id}/logs
          API.
          * **COMPLETED**: The job completed successfully.
          * **CREATED**: The job was created, but the provisioning, modification, or
          removal of IBM Cloud resources has not started yet.
          * **FAILED**: An error occurred during the plan, apply, or destroy job. Use the
          job ID to retrieve the URL to the log files for your job.
          * **IN PROGRESS**: The job is in progress. You can use the log_url to access the
          logs.
    :attr str template_id: (optional) The ID that was assigned to your Terraform
          template or IBM Cloud catalog software template.
    :attr str template_type: (optional) The type of template.
    """

    def __init__(self,
                 *,
                 end_time: datetime = None,
                 log_summary: 'LogSummary' = None,
                 log_url: str = None,
                 message: str = None,
                 start_time: datetime = None,
                 status: str = None,
                 template_id: str = None,
                 template_type: str = None) -> None:
        """
        Initialize a WorkspaceActivityTemplate object.

        :param datetime end_time: (optional) End time for the job.
        :param LogSummary log_summary: (optional) Summary information extracted
               from the job logs.
        :param str log_url: (optional) Log URL.
        :param str message: (optional) Message.
        :param datetime start_time: (optional) Job start time.
        :param str status: (optional) The status of your activity or job. To
               retrieve the URL to your job logs, use the GET
               /v1/workspaces/{id}/actions/{action_id}/logs API.
               * **COMPLETED**: The job completed successfully.
               * **CREATED**: The job was created, but the provisioning, modification, or
               removal of IBM Cloud resources has not started yet.
               * **FAILED**: An error occurred during the plan, apply, or destroy job. Use
               the job ID to retrieve the URL to the log files for your job.
               * **IN PROGRESS**: The job is in progress. You can use the log_url to
               access the logs.
        :param str template_id: (optional) The ID that was assigned to your
               Terraform template or IBM Cloud catalog software template.
        :param str template_type: (optional) The type of template.
        """
        self.end_time = end_time
        self.log_summary = log_summary
        self.log_url = log_url
        self.message = message
        self.start_time = start_time
        self.status = status
        self.template_id = template_id
        self.template_type = template_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityTemplate':
        """Initialize a WorkspaceActivityTemplate object from a json dictionary."""
        args = {}
        if 'end_time' in _dict:
            args['end_time'] = string_to_datetime(_dict.get('end_time'))
        if 'log_summary' in _dict:
            args['log_summary'] = LogSummary.from_dict(_dict.get('log_summary'))
        if 'log_url' in _dict:
            args['log_url'] = _dict.get('log_url')
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'start_time' in _dict:
            args['start_time'] = string_to_datetime(_dict.get('start_time'))
        if 'status' in _dict:
            args['status'] = _dict.get('status')
        if 'template_id' in _dict:
            args['template_id'] = _dict.get('template_id')
        if 'template_type' in _dict:
            args['template_type'] = _dict.get('template_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityTemplate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'end_time') and self.end_time is not None:
            _dict['end_time'] = datetime_to_string(self.end_time)
        if hasattr(self, 'log_summary') and self.log_summary is not None:
            _dict['log_summary'] = self.log_summary.to_dict()
        if hasattr(self, 'log_url') and self.log_url is not None:
            _dict['log_url'] = self.log_url
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'start_time') and self.start_time is not None:
            _dict['start_time'] = datetime_to_string(self.start_time)
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'template_id') and self.template_id is not None:
            _dict['template_id'] = self.template_id
        if hasattr(self, 'template_type') and self.template_type is not None:
            _dict['template_type'] = self.template_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityTemplate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityTemplate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityTemplate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceActivityTemplateLogs():
    """
    Information about the log URL for a job that ran for a template against your
    workspace.

    :attr str log_url: (optional) The URL to access the logs that were created
          during the plan, apply, or destroy job.
    :attr str template_id: (optional) The ID that was assigned to your Terraform
          template or IBM Cloud catalog software template.
    :attr str template_type: (optional) The type of template.
    """

    def __init__(self,
                 *,
                 log_url: str = None,
                 template_id: str = None,
                 template_type: str = None) -> None:
        """
        Initialize a WorkspaceActivityTemplateLogs object.

        :param str log_url: (optional) The URL to access the logs that were created
               during the plan, apply, or destroy job.
        :param str template_id: (optional) The ID that was assigned to your
               Terraform template or IBM Cloud catalog software template.
        :param str template_type: (optional) The type of template.
        """
        self.log_url = log_url
        self.template_id = template_id
        self.template_type = template_type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceActivityTemplateLogs':
        """Initialize a WorkspaceActivityTemplateLogs object from a json dictionary."""
        args = {}
        if 'log_url' in _dict:
            args['log_url'] = _dict.get('log_url')
        if 'template_id' in _dict:
            args['template_id'] = _dict.get('template_id')
        if 'template_type' in _dict:
            args['template_type'] = _dict.get('template_type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceActivityTemplateLogs object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'log_url') and self.log_url is not None:
            _dict['log_url'] = self.log_url
        if hasattr(self, 'template_id') and self.template_id is not None:
            _dict['template_id'] = self.template_id
        if hasattr(self, 'template_type') and self.template_type is not None:
            _dict['template_type'] = self.template_type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceActivityTemplateLogs object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceActivityTemplateLogs') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceActivityTemplateLogs') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceBulkDeleteResponse():
    """
    Response after successfully initiating the bulk job to delete multiple workspaces.

    :attr str job: (optional) Workspace deletion job name.
    :attr str job_id: (optional) Workspace deletion job id.
    """

    def __init__(self,
                 *,
                 job: str = None,
                 job_id: str = None) -> None:
        """
        Initialize a WorkspaceBulkDeleteResponse object.

        :param str job: (optional) Workspace deletion job name.
        :param str job_id: (optional) Workspace deletion job id.
        """
        self.job = job
        self.job_id = job_id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceBulkDeleteResponse':
        """Initialize a WorkspaceBulkDeleteResponse object from a json dictionary."""
        args = {}
        if 'job' in _dict:
            args['job'] = _dict.get('job')
        if 'job_id' in _dict:
            args['job_id'] = _dict.get('job_id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceBulkDeleteResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job') and self.job is not None:
            _dict['job'] = self.job
        if hasattr(self, 'job_id') and self.job_id is not None:
            _dict['job_id'] = self.job_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceBulkDeleteResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceBulkDeleteResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceBulkDeleteResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceJobResponse():
    """
    Response from the workspace bulk job status.

    :attr WorkspaceJobStatusType job_status: (optional) Status of the workspace bulk
          job.
    """

    def __init__(self,
                 *,
                 job_status: 'WorkspaceJobStatusType' = None) -> None:
        """
        Initialize a WorkspaceJobResponse object.

        :param WorkspaceJobStatusType job_status: (optional) Status of the
               workspace bulk job.
        """
        self.job_status = job_status

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceJobResponse':
        """Initialize a WorkspaceJobResponse object from a json dictionary."""
        args = {}
        if 'job_status' in _dict:
            args['job_status'] = WorkspaceJobStatusType.from_dict(_dict.get('job_status'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceJobResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'job_status') and self.job_status is not None:
            _dict['job_status'] = self.job_status.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceJobResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceJobResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceJobResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceJobStatusType():
    """
    Status of the workspace bulk job.

    :attr List[str] failed: (optional) List of failed workspace jobs.
    :attr List[str] in_progress: (optional) List of in_progress workspace jobs.
    :attr List[str] success: (optional) List of successful workspace jobs.
    :attr datetime last_updated_on: (optional) Workspace job status updated at.
    """

    def __init__(self,
                 *,
                 failed: List[str] = None,
                 in_progress: List[str] = None,
                 success: List[str] = None,
                 last_updated_on: datetime = None) -> None:
        """
        Initialize a WorkspaceJobStatusType object.

        :param List[str] failed: (optional) List of failed workspace jobs.
        :param List[str] in_progress: (optional) List of in_progress workspace
               jobs.
        :param List[str] success: (optional) List of successful workspace jobs.
        :param datetime last_updated_on: (optional) Workspace job status updated
               at.
        """
        self.failed = failed
        self.in_progress = in_progress
        self.success = success
        self.last_updated_on = last_updated_on

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceJobStatusType':
        """Initialize a WorkspaceJobStatusType object from a json dictionary."""
        args = {}
        if 'failed' in _dict:
            args['failed'] = _dict.get('failed')
        if 'in_progress' in _dict:
            args['in_progress'] = _dict.get('in_progress')
        if 'success' in _dict:
            args['success'] = _dict.get('success')
        if 'last_updated_on' in _dict:
            args['last_updated_on'] = string_to_datetime(_dict.get('last_updated_on'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceJobStatusType object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'failed') and self.failed is not None:
            _dict['failed'] = self.failed
        if hasattr(self, 'in_progress') and self.in_progress is not None:
            _dict['in_progress'] = self.in_progress
        if hasattr(self, 'success') and self.success is not None:
            _dict['success'] = self.success
        if hasattr(self, 'last_updated_on') and self.last_updated_on is not None:
            _dict['last_updated_on'] = datetime_to_string(self.last_updated_on)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceJobStatusType object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceJobStatusType') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceJobStatusType') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceResponse():
    """
    Workspace details.

    :attr List[str] applied_shareddata_ids: (optional) List of applied shared
          dataset ID.
    :attr CatalogRef catalog_ref: (optional) Information about the software template
          that you chose from the IBM Cloud catalog. This information is returned for IBM
          Cloud catalog offerings only.
    :attr datetime created_at: (optional) The timestamp when the workspace was
          created.
    :attr str created_by: (optional) The user ID that created the workspace.
    :attr str crn: (optional) The workspace CRN.
    :attr str description: (optional) The description of the workspace.
    :attr str id: (optional) The unique identifier of the workspace.
    :attr datetime last_health_check_at: (optional) The timestamp when the last
          health check was performed by Schematics.
    :attr str location: (optional) The IBM Cloud location where your workspace was
          provisioned.
    :attr str name: (optional) The name of the workspace.
    :attr str resource_group: (optional) The resource group the workspace was
          provisioned in.
    :attr List[TemplateRunTimeDataResponse] runtime_data: (optional) Information
          about the provisioning engine, state file, and runtime logs.
    :attr SharedTargetDataResponse shared_data: (optional) Information about the
          Target used by the templates originating from IBM Cloud catalog offerings. This
          information is not relevant when you create a workspace from your own Terraform
          template.
    :attr str status: (optional) The status of the workspace.
            **Active**: After you successfully ran your infrastructure code by applying
          your Terraform execution plan, the state of your workspace changes to `Active`.
            **Connecting**: Schematics tries to connect to the template in your source
          repo. If successfully connected, the template is downloaded and metadata, such
          as input parameters, is extracted. After the template is downloaded, the state
          of the workspace changes to `Scanning`.
            **Draft**: The workspace is created without a reference to a GitHub or GitLab
          repository.
            **Failed**: If errors occur during the execution of your infrastructure code
          in IBM Cloud Schematics, your workspace status is set to `Failed`.
            **Inactive**: The Terraform template was scanned successfully and the
          workspace creation is complete. You can now start running Schematics plan and
          apply jobs to provision the IBM Cloud resources that you specified in your
          template. If you have an `Active` workspace and decide to remove all your
          resources, your workspace is set to `Inactive` after all your resources are
          removed.
            **In progress**: When you instruct IBM Cloud Schematics to run your
          infrastructure code by applying your Terraform execution plan, the status of our
          workspace changes to `In progress`.
            **Scanning**: The download of the Terraform template is complete and
          vulnerability scanning started. If the scan is successful, the workspace state
          changes to `Inactive`. If errors in your template are found, the state changes
          to `Template Error`.
            **Stopped**: The Schematics plan, apply, or destroy job was cancelled
          manually.
            **Template Error**: The Schematics template contains errors and cannot be
          processed.
    :attr List[str] tags: (optional) A list of tags that are associated with the
          workspace.
    :attr List[TemplateSourceDataResponse] template_data: (optional) Information
          about the Terraform or IBM Cloud software template that you want to use.
    :attr str template_ref: (optional) Workspace template reference.
    :attr TemplateRepoResponse template_repo: (optional) Information about the
          Template repository used by the workspace.
    :attr List[str] type: (optional) The Terraform version that was used to run your
          Terraform code.
    :attr datetime updated_at: (optional) The timestamp when the workspace was last
          updated.
    :attr str updated_by: (optional) The user ID that updated the workspace.
    :attr WorkspaceStatusResponse workspace_status: (optional) Response that
          indicate the status of the workspace as either frozen or locked.
    :attr WorkspaceStatusMessage workspace_status_msg: (optional) Information about
          the last job that ran against the workspace. -.
    """

    def __init__(self,
                 *,
                 applied_shareddata_ids: List[str] = None,
                 catalog_ref: 'CatalogRef' = None,
                 created_at: datetime = None,
                 created_by: str = None,
                 crn: str = None,
                 description: str = None,
                 id: str = None,
                 last_health_check_at: datetime = None,
                 location: str = None,
                 name: str = None,
                 resource_group: str = None,
                 runtime_data: List['TemplateRunTimeDataResponse'] = None,
                 shared_data: 'SharedTargetDataResponse' = None,
                 status: str = None,
                 tags: List[str] = None,
                 template_data: List['TemplateSourceDataResponse'] = None,
                 template_ref: str = None,
                 template_repo: 'TemplateRepoResponse' = None,
                 type: List[str] = None,
                 updated_at: datetime = None,
                 updated_by: str = None,
                 workspace_status: 'WorkspaceStatusResponse' = None,
                 workspace_status_msg: 'WorkspaceStatusMessage' = None) -> None:
        """
        Initialize a WorkspaceResponse object.

        :param List[str] applied_shareddata_ids: (optional) List of applied shared
               dataset ID.
        :param CatalogRef catalog_ref: (optional) Information about the software
               template that you chose from the IBM Cloud catalog. This information is
               returned for IBM Cloud catalog offerings only.
        :param datetime created_at: (optional) The timestamp when the workspace was
               created.
        :param str created_by: (optional) The user ID that created the workspace.
        :param str crn: (optional) The workspace CRN.
        :param str description: (optional) The description of the workspace.
        :param str id: (optional) The unique identifier of the workspace.
        :param datetime last_health_check_at: (optional) The timestamp when the
               last health check was performed by Schematics.
        :param str location: (optional) The IBM Cloud location where your workspace
               was provisioned.
        :param str name: (optional) The name of the workspace.
        :param str resource_group: (optional) The resource group the workspace was
               provisioned in.
        :param List[TemplateRunTimeDataResponse] runtime_data: (optional)
               Information about the provisioning engine, state file, and runtime logs.
        :param SharedTargetDataResponse shared_data: (optional) Information about
               the Target used by the templates originating from IBM Cloud catalog
               offerings. This information is not relevant when you create a workspace
               from your own Terraform template.
        :param str status: (optional) The status of the workspace.
                 **Active**: After you successfully ran your infrastructure code by
               applying your Terraform execution plan, the state of your workspace changes
               to `Active`.
                 **Connecting**: Schematics tries to connect to the template in your
               source repo. If successfully connected, the template is downloaded and
               metadata, such as input parameters, is extracted. After the template is
               downloaded, the state of the workspace changes to `Scanning`.
                 **Draft**: The workspace is created without a reference to a GitHub or
               GitLab repository.
                 **Failed**: If errors occur during the execution of your infrastructure
               code in IBM Cloud Schematics, your workspace status is set to `Failed`.
                 **Inactive**: The Terraform template was scanned successfully and the
               workspace creation is complete. You can now start running Schematics plan
               and apply jobs to provision the IBM Cloud resources that you specified in
               your template. If you have an `Active` workspace and decide to remove all
               your resources, your workspace is set to `Inactive` after all your
               resources are removed.
                 **In progress**: When you instruct IBM Cloud Schematics to run your
               infrastructure code by applying your Terraform execution plan, the status
               of our workspace changes to `In progress`.
                 **Scanning**: The download of the Terraform template is complete and
               vulnerability scanning started. If the scan is successful, the workspace
               state changes to `Inactive`. If errors in your template are found, the
               state changes to `Template Error`.
                 **Stopped**: The Schematics plan, apply, or destroy job was cancelled
               manually.
                 **Template Error**: The Schematics template contains errors and cannot be
               processed.
        :param List[str] tags: (optional) A list of tags that are associated with
               the workspace.
        :param List[TemplateSourceDataResponse] template_data: (optional)
               Information about the Terraform or IBM Cloud software template that you
               want to use.
        :param str template_ref: (optional) Workspace template reference.
        :param TemplateRepoResponse template_repo: (optional) Information about the
               Template repository used by the workspace.
        :param List[str] type: (optional) The Terraform version that was used to
               run your Terraform code.
        :param datetime updated_at: (optional) The timestamp when the workspace was
               last updated.
        :param str updated_by: (optional) The user ID that updated the workspace.
        :param WorkspaceStatusResponse workspace_status: (optional) Response that
               indicate the status of the workspace as either frozen or locked.
        :param WorkspaceStatusMessage workspace_status_msg: (optional) Information
               about the last job that ran against the workspace. -.
        """
        self.applied_shareddata_ids = applied_shareddata_ids
        self.catalog_ref = catalog_ref
        self.created_at = created_at
        self.created_by = created_by
        self.crn = crn
        self.description = description
        self.id = id
        self.last_health_check_at = last_health_check_at
        self.location = location
        self.name = name
        self.resource_group = resource_group
        self.runtime_data = runtime_data
        self.shared_data = shared_data
        self.status = status
        self.tags = tags
        self.template_data = template_data
        self.template_ref = template_ref
        self.template_repo = template_repo
        self.type = type
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.workspace_status = workspace_status
        self.workspace_status_msg = workspace_status_msg

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceResponse':
        """Initialize a WorkspaceResponse object from a json dictionary."""
        args = {}
        if 'applied_shareddata_ids' in _dict:
            args['applied_shareddata_ids'] = _dict.get('applied_shareddata_ids')
        if 'catalog_ref' in _dict:
            args['catalog_ref'] = CatalogRef.from_dict(_dict.get('catalog_ref'))
        if 'created_at' in _dict:
            args['created_at'] = string_to_datetime(_dict.get('created_at'))
        if 'created_by' in _dict:
            args['created_by'] = _dict.get('created_by')
        if 'crn' in _dict:
            args['crn'] = _dict.get('crn')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'last_health_check_at' in _dict:
            args['last_health_check_at'] = string_to_datetime(_dict.get('last_health_check_at'))
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'resource_group' in _dict:
            args['resource_group'] = _dict.get('resource_group')
        if 'runtime_data' in _dict:
            args['runtime_data'] = [TemplateRunTimeDataResponse.from_dict(x) for x in _dict.get('runtime_data')]
        if 'shared_data' in _dict:
            args['shared_data'] = SharedTargetDataResponse.from_dict(_dict.get('shared_data'))
        if 'status' in _dict:
            args['status'] = _dict.get('status')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'template_data' in _dict:
            args['template_data'] = [TemplateSourceDataResponse.from_dict(x) for x in _dict.get('template_data')]
        if 'template_ref' in _dict:
            args['template_ref'] = _dict.get('template_ref')
        if 'template_repo' in _dict:
            args['template_repo'] = TemplateRepoResponse.from_dict(_dict.get('template_repo'))
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'updated_at' in _dict:
            args['updated_at'] = string_to_datetime(_dict.get('updated_at'))
        if 'updated_by' in _dict:
            args['updated_by'] = _dict.get('updated_by')
        if 'workspace_status' in _dict:
            args['workspace_status'] = WorkspaceStatusResponse.from_dict(_dict.get('workspace_status'))
        if 'workspace_status_msg' in _dict:
            args['workspace_status_msg'] = WorkspaceStatusMessage.from_dict(_dict.get('workspace_status_msg'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'applied_shareddata_ids') and self.applied_shareddata_ids is not None:
            _dict['applied_shareddata_ids'] = self.applied_shareddata_ids
        if hasattr(self, 'catalog_ref') and self.catalog_ref is not None:
            _dict['catalog_ref'] = self.catalog_ref.to_dict()
        if hasattr(self, 'created_at') and self.created_at is not None:
            _dict['created_at'] = datetime_to_string(self.created_at)
        if hasattr(self, 'created_by') and self.created_by is not None:
            _dict['created_by'] = self.created_by
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['crn'] = self.crn
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'last_health_check_at') and self.last_health_check_at is not None:
            _dict['last_health_check_at'] = datetime_to_string(self.last_health_check_at)
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'resource_group') and self.resource_group is not None:
            _dict['resource_group'] = self.resource_group
        if hasattr(self, 'runtime_data') and self.runtime_data is not None:
            _dict['runtime_data'] = [x.to_dict() for x in self.runtime_data]
        if hasattr(self, 'shared_data') and self.shared_data is not None:
            _dict['shared_data'] = self.shared_data.to_dict()
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'template_data') and self.template_data is not None:
            _dict['template_data'] = [x.to_dict() for x in self.template_data]
        if hasattr(self, 'template_ref') and self.template_ref is not None:
            _dict['template_ref'] = self.template_ref
        if hasattr(self, 'template_repo') and self.template_repo is not None:
            _dict['template_repo'] = self.template_repo.to_dict()
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'updated_at') and self.updated_at is not None:
            _dict['updated_at'] = datetime_to_string(self.updated_at)
        if hasattr(self, 'updated_by') and self.updated_by is not None:
            _dict['updated_by'] = self.updated_by
        if hasattr(self, 'workspace_status') and self.workspace_status is not None:
            _dict['workspace_status'] = self.workspace_status.to_dict()
        if hasattr(self, 'workspace_status_msg') and self.workspace_status_msg is not None:
            _dict['workspace_status_msg'] = self.workspace_status_msg.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceResponseList():
    """
    List of workspaces.

    :attr int count: (optional) The number of workspaces in the IBM Cloud account
          that you have access to and that matched your search criteria.
    :attr int limit: The `limit` value that you set in your API request and that
          represents the maximum number of workspaces that you wanted to list.
    :attr int offset: The `offset` value that you set in your API request. The
          offset value represents the position number of the workspace from which you
          wanted to start listing your workspaces.
    :attr List[WorkspaceResponse] workspaces: (optional) The list of workspaces that
          was included in your API response.
    """

    def __init__(self,
                 limit: int,
                 offset: int,
                 *,
                 count: int = None,
                 workspaces: List['WorkspaceResponse'] = None) -> None:
        """
        Initialize a WorkspaceResponseList object.

        :param int limit: The `limit` value that you set in your API request and
               that represents the maximum number of workspaces that you wanted to list.
        :param int offset: The `offset` value that you set in your API request. The
               offset value represents the position number of the workspace from which you
               wanted to start listing your workspaces.
        :param int count: (optional) The number of workspaces in the IBM Cloud
               account that you have access to and that matched your search criteria.
        :param List[WorkspaceResponse] workspaces: (optional) The list of
               workspaces that was included in your API response.
        """
        self.count = count
        self.limit = limit
        self.offset = offset
        self.workspaces = workspaces

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceResponseList':
        """Initialize a WorkspaceResponseList object from a json dictionary."""
        args = {}
        if 'count' in _dict:
            args['count'] = _dict.get('count')
        if 'limit' in _dict:
            args['limit'] = _dict.get('limit')
        else:
            raise ValueError('Required property \'limit\' not present in WorkspaceResponseList JSON')
        if 'offset' in _dict:
            args['offset'] = _dict.get('offset')
        else:
            raise ValueError('Required property \'offset\' not present in WorkspaceResponseList JSON')
        if 'workspaces' in _dict:
            args['workspaces'] = [WorkspaceResponse.from_dict(x) for x in _dict.get('workspaces')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceResponseList object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'count') and self.count is not None:
            _dict['count'] = self.count
        if hasattr(self, 'limit') and self.limit is not None:
            _dict['limit'] = self.limit
        if hasattr(self, 'offset') and self.offset is not None:
            _dict['offset'] = self.offset
        if hasattr(self, 'workspaces') and self.workspaces is not None:
            _dict['workspaces'] = [x.to_dict() for x in self.workspaces]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceResponseList object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceResponseList') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceResponseList') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceStatusMessage():
    """
    Information about the last job that ran against the workspace. -.

    :attr str status_code: (optional) The success or error code that was returned
          for the last plan, apply, or destroy job that ran against your workspace.
    :attr str status_msg: (optional) The success or error message that was returned
          for the last plan, apply, or destroy job that ran against your workspace.
    """

    def __init__(self,
                 *,
                 status_code: str = None,
                 status_msg: str = None) -> None:
        """
        Initialize a WorkspaceStatusMessage object.

        :param str status_code: (optional) The success or error code that was
               returned for the last plan, apply, or destroy job that ran against your
               workspace.
        :param str status_msg: (optional) The success or error message that was
               returned for the last plan, apply, or destroy job that ran against your
               workspace.
        """
        self.status_code = status_code
        self.status_msg = status_msg

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceStatusMessage':
        """Initialize a WorkspaceStatusMessage object from a json dictionary."""
        args = {}
        if 'status_code' in _dict:
            args['status_code'] = _dict.get('status_code')
        if 'status_msg' in _dict:
            args['status_msg'] = _dict.get('status_msg')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceStatusMessage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'status_code') and self.status_code is not None:
            _dict['status_code'] = self.status_code
        if hasattr(self, 'status_msg') and self.status_msg is not None:
            _dict['status_msg'] = self.status_msg
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceStatusMessage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceStatusMessage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceStatusMessage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceStatusRequest():
    """
    WorkspaceStatusRequest -.

    :attr bool frozen: (optional) If set to true, the workspace is frozen and
          changes to the workspace are disabled.
    :attr datetime frozen_at: (optional) The timestamp when the workspace was
          frozen.
    :attr str frozen_by: (optional) The user ID that froze the workspace.
    :attr bool locked: (optional) If set to true, the workspace is locked and
          disabled for changes.
    :attr str locked_by: (optional) The user ID that initiated a resource-related
          job, such as applying or destroying resources, that locked the workspace.
    :attr datetime locked_time: (optional) The timestamp when the workspace was
          locked.
    """

    def __init__(self,
                 *,
                 frozen: bool = None,
                 frozen_at: datetime = None,
                 frozen_by: str = None,
                 locked: bool = None,
                 locked_by: str = None,
                 locked_time: datetime = None) -> None:
        """
        Initialize a WorkspaceStatusRequest object.

        :param bool frozen: (optional) If set to true, the workspace is frozen and
               changes to the workspace are disabled.
        :param datetime frozen_at: (optional) The timestamp when the workspace was
               frozen.
        :param str frozen_by: (optional) The user ID that froze the workspace.
        :param bool locked: (optional) If set to true, the workspace is locked and
               disabled for changes.
        :param str locked_by: (optional) The user ID that initiated a
               resource-related job, such as applying or destroying resources, that locked
               the workspace.
        :param datetime locked_time: (optional) The timestamp when the workspace
               was locked.
        """
        self.frozen = frozen
        self.frozen_at = frozen_at
        self.frozen_by = frozen_by
        self.locked = locked
        self.locked_by = locked_by
        self.locked_time = locked_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceStatusRequest':
        """Initialize a WorkspaceStatusRequest object from a json dictionary."""
        args = {}
        if 'frozen' in _dict:
            args['frozen'] = _dict.get('frozen')
        if 'frozen_at' in _dict:
            args['frozen_at'] = string_to_datetime(_dict.get('frozen_at'))
        if 'frozen_by' in _dict:
            args['frozen_by'] = _dict.get('frozen_by')
        if 'locked' in _dict:
            args['locked'] = _dict.get('locked')
        if 'locked_by' in _dict:
            args['locked_by'] = _dict.get('locked_by')
        if 'locked_time' in _dict:
            args['locked_time'] = string_to_datetime(_dict.get('locked_time'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceStatusRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'frozen') and self.frozen is not None:
            _dict['frozen'] = self.frozen
        if hasattr(self, 'frozen_at') and self.frozen_at is not None:
            _dict['frozen_at'] = datetime_to_string(self.frozen_at)
        if hasattr(self, 'frozen_by') and self.frozen_by is not None:
            _dict['frozen_by'] = self.frozen_by
        if hasattr(self, 'locked') and self.locked is not None:
            _dict['locked'] = self.locked
        if hasattr(self, 'locked_by') and self.locked_by is not None:
            _dict['locked_by'] = self.locked_by
        if hasattr(self, 'locked_time') and self.locked_time is not None:
            _dict['locked_time'] = datetime_to_string(self.locked_time)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceStatusRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceStatusRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceStatusRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceStatusResponse():
    """
    Response that indicate the status of the workspace as either frozen or locked.

    :attr bool frozen: (optional) If set to true, the workspace is frozen and
          changes to the workspace are disabled.
    :attr datetime frozen_at: (optional) The timestamp when the workspace was
          frozen.
    :attr str frozen_by: (optional) The user ID that froze the workspace.
    :attr bool locked: (optional) If set to true, the workspace is locked and
          disabled for changes.
    :attr str locked_by: (optional) The user ID that initiated a resource-related
          job, such as applying or destroying resources, that locked the workspace.
    :attr datetime locked_time: (optional) The timestamp when the workspace was
          locked.
    """

    def __init__(self,
                 *,
                 frozen: bool = None,
                 frozen_at: datetime = None,
                 frozen_by: str = None,
                 locked: bool = None,
                 locked_by: str = None,
                 locked_time: datetime = None) -> None:
        """
        Initialize a WorkspaceStatusResponse object.

        :param bool frozen: (optional) If set to true, the workspace is frozen and
               changes to the workspace are disabled.
        :param datetime frozen_at: (optional) The timestamp when the workspace was
               frozen.
        :param str frozen_by: (optional) The user ID that froze the workspace.
        :param bool locked: (optional) If set to true, the workspace is locked and
               disabled for changes.
        :param str locked_by: (optional) The user ID that initiated a
               resource-related job, such as applying or destroying resources, that locked
               the workspace.
        :param datetime locked_time: (optional) The timestamp when the workspace
               was locked.
        """
        self.frozen = frozen
        self.frozen_at = frozen_at
        self.frozen_by = frozen_by
        self.locked = locked
        self.locked_by = locked_by
        self.locked_time = locked_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceStatusResponse':
        """Initialize a WorkspaceStatusResponse object from a json dictionary."""
        args = {}
        if 'frozen' in _dict:
            args['frozen'] = _dict.get('frozen')
        if 'frozen_at' in _dict:
            args['frozen_at'] = string_to_datetime(_dict.get('frozen_at'))
        if 'frozen_by' in _dict:
            args['frozen_by'] = _dict.get('frozen_by')
        if 'locked' in _dict:
            args['locked'] = _dict.get('locked')
        if 'locked_by' in _dict:
            args['locked_by'] = _dict.get('locked_by')
        if 'locked_time' in _dict:
            args['locked_time'] = string_to_datetime(_dict.get('locked_time'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceStatusResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'frozen') and self.frozen is not None:
            _dict['frozen'] = self.frozen
        if hasattr(self, 'frozen_at') and self.frozen_at is not None:
            _dict['frozen_at'] = datetime_to_string(self.frozen_at)
        if hasattr(self, 'frozen_by') and self.frozen_by is not None:
            _dict['frozen_by'] = self.frozen_by
        if hasattr(self, 'locked') and self.locked is not None:
            _dict['locked'] = self.locked
        if hasattr(self, 'locked_by') and self.locked_by is not None:
            _dict['locked_by'] = self.locked_by
        if hasattr(self, 'locked_time') and self.locked_time is not None:
            _dict['locked_time'] = datetime_to_string(self.locked_time)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceStatusResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceStatusResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceStatusResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceStatusUpdateRequest():
    """
    Input to update the workspace status.

    :attr bool frozen: (optional) If set to true, the workspace is frozen and
          changes to the workspace are disabled.
    :attr datetime frozen_at: (optional) Frozen at.
    :attr str frozen_by: (optional) Frozen by.
    :attr bool locked: (optional) Locked status.
    :attr str locked_by: (optional) Locked by.
    :attr datetime locked_time: (optional) Locked at.
    """

    def __init__(self,
                 *,
                 frozen: bool = None,
                 frozen_at: datetime = None,
                 frozen_by: str = None,
                 locked: bool = None,
                 locked_by: str = None,
                 locked_time: datetime = None) -> None:
        """
        Initialize a WorkspaceStatusUpdateRequest object.

        :param bool frozen: (optional) If set to true, the workspace is frozen and
               changes to the workspace are disabled.
        :param datetime frozen_at: (optional) Frozen at.
        :param str frozen_by: (optional) Frozen by.
        :param bool locked: (optional) Locked status.
        :param str locked_by: (optional) Locked by.
        :param datetime locked_time: (optional) Locked at.
        """
        self.frozen = frozen
        self.frozen_at = frozen_at
        self.frozen_by = frozen_by
        self.locked = locked
        self.locked_by = locked_by
        self.locked_time = locked_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceStatusUpdateRequest':
        """Initialize a WorkspaceStatusUpdateRequest object from a json dictionary."""
        args = {}
        if 'frozen' in _dict:
            args['frozen'] = _dict.get('frozen')
        if 'frozen_at' in _dict:
            args['frozen_at'] = string_to_datetime(_dict.get('frozen_at'))
        if 'frozen_by' in _dict:
            args['frozen_by'] = _dict.get('frozen_by')
        if 'locked' in _dict:
            args['locked'] = _dict.get('locked')
        if 'locked_by' in _dict:
            args['locked_by'] = _dict.get('locked_by')
        if 'locked_time' in _dict:
            args['locked_time'] = string_to_datetime(_dict.get('locked_time'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceStatusUpdateRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'frozen') and self.frozen is not None:
            _dict['frozen'] = self.frozen
        if hasattr(self, 'frozen_at') and self.frozen_at is not None:
            _dict['frozen_at'] = datetime_to_string(self.frozen_at)
        if hasattr(self, 'frozen_by') and self.frozen_by is not None:
            _dict['frozen_by'] = self.frozen_by
        if hasattr(self, 'locked') and self.locked is not None:
            _dict['locked'] = self.locked
        if hasattr(self, 'locked_by') and self.locked_by is not None:
            _dict['locked_by'] = self.locked_by
        if hasattr(self, 'locked_time') and self.locked_time is not None:
            _dict['locked_time'] = datetime_to_string(self.locked_time)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceStatusUpdateRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceStatusUpdateRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceStatusUpdateRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceTemplateValuesResponse():
    """
    Response with the template details in your workspace.

    :attr List[TemplateRunTimeDataResponse] runtime_data: (optional) Information
          about the provisioning engine, state file, and runtime logs.
    :attr SharedTargetData shared_data: (optional) Information about the Target used
          by the templates originating from the  IBM Cloud catalog offerings. This
          information is not relevant for workspace created using your own Terraform
          template.
    :attr List[TemplateSourceDataResponse] template_data: (optional) Information
          about the input variables that are used in the template.
    """

    def __init__(self,
                 *,
                 runtime_data: List['TemplateRunTimeDataResponse'] = None,
                 shared_data: 'SharedTargetData' = None,
                 template_data: List['TemplateSourceDataResponse'] = None) -> None:
        """
        Initialize a WorkspaceTemplateValuesResponse object.

        :param List[TemplateRunTimeDataResponse] runtime_data: (optional)
               Information about the provisioning engine, state file, and runtime logs.
        :param SharedTargetData shared_data: (optional) Information about the
               Target used by the templates originating from the  IBM Cloud catalog
               offerings. This information is not relevant for workspace created using
               your own Terraform template.
        :param List[TemplateSourceDataResponse] template_data: (optional)
               Information about the input variables that are used in the template.
        """
        self.runtime_data = runtime_data
        self.shared_data = shared_data
        self.template_data = template_data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceTemplateValuesResponse':
        """Initialize a WorkspaceTemplateValuesResponse object from a json dictionary."""
        args = {}
        if 'runtime_data' in _dict:
            args['runtime_data'] = [TemplateRunTimeDataResponse.from_dict(x) for x in _dict.get('runtime_data')]
        if 'shared_data' in _dict:
            args['shared_data'] = SharedTargetData.from_dict(_dict.get('shared_data'))
        if 'template_data' in _dict:
            args['template_data'] = [TemplateSourceDataResponse.from_dict(x) for x in _dict.get('template_data')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceTemplateValuesResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'runtime_data') and self.runtime_data is not None:
            _dict['runtime_data'] = [x.to_dict() for x in self.runtime_data]
        if hasattr(self, 'shared_data') and self.shared_data is not None:
            _dict['shared_data'] = self.shared_data.to_dict()
        if hasattr(self, 'template_data') and self.template_data is not None:
            _dict['template_data'] = [x.to_dict() for x in self.template_data]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceTemplateValuesResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceTemplateValuesResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceTemplateValuesResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceVariableRequest():
    """
    Input variables for your workspace.

    :attr str description: (optional) The description of your input variable.
    :attr str name: (optional) The name of the variable.
    :attr bool secure: (optional) If set to `true`, the value of your input variable
          is protected and not returned in your API response.
    :attr str type: (optional) `Terraform v0.11` supports `string`, `list`, `map`
          data type. For more information, about the syntax, see [Configuring input
          variables](https://www.terraform.io/docs/configuration-0-11/variables.html).
          <br> `Terraform v0.12` additionally, supports `bool`, `number` and complex data
          types such as `list(type)`, `map(type)`,
          `object({attribute name=type,..})`, `set(type)`, `tuple([type])`. For more
          information, about the syntax to use the complex data type, see [Configuring
          variables](https://www.terraform.io/docs/configuration/variables.html#type-constraints).
    :attr bool use_default: (optional) Variable uses default value; and is not
          over-ridden.
    :attr str value: (optional) Enter the value as a string for the primitive types
          such as `bool`, `number`, `string`, and `HCL` format for the complex variables,
          as you provide in a `.tfvars` file. **You need to enter escaped string of `HCL`
          format for the complex variable value**. For more information, about how to
          declare variables in a terraform configuration file and provide value to
          schematics, see [Providing values for the declared
          variables](https://cloud.ibm.com/docs/schematics?topic=schematics-create-tf-config#declare-variable).
    """

    def __init__(self,
                 *,
                 description: str = None,
                 name: str = None,
                 secure: bool = None,
                 type: str = None,
                 use_default: bool = None,
                 value: str = None) -> None:
        """
        Initialize a WorkspaceVariableRequest object.

        :param str description: (optional) The description of your input variable.
        :param str name: (optional) The name of the variable.
        :param bool secure: (optional) If set to `true`, the value of your input
               variable is protected and not returned in your API response.
        :param str type: (optional) `Terraform v0.11` supports `string`, `list`,
               `map` data type. For more information, about the syntax, see [Configuring
               input
               variables](https://www.terraform.io/docs/configuration-0-11/variables.html).
               <br> `Terraform v0.12` additionally, supports `bool`, `number` and complex
               data types such as `list(type)`, `map(type)`,
               `object({attribute name=type,..})`, `set(type)`, `tuple([type])`. For more
               information, about the syntax to use the complex data type, see
               [Configuring
               variables](https://www.terraform.io/docs/configuration/variables.html#type-constraints).
        :param bool use_default: (optional) Variable uses default value; and is not
               over-ridden.
        :param str value: (optional) Enter the value as a string for the primitive
               types such as `bool`, `number`, `string`, and `HCL` format for the complex
               variables, as you provide in a `.tfvars` file. **You need to enter escaped
               string of `HCL` format for the complex variable value**. For more
               information, about how to declare variables in a terraform configuration
               file and provide value to schematics, see [Providing values for the
               declared
               variables](https://cloud.ibm.com/docs/schematics?topic=schematics-create-tf-config#declare-variable).
        """
        self.description = description
        self.name = name
        self.secure = secure
        self.type = type
        self.use_default = use_default
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceVariableRequest':
        """Initialize a WorkspaceVariableRequest object from a json dictionary."""
        args = {}
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'use_default' in _dict:
            args['use_default'] = _dict.get('use_default')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceVariableRequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'use_default') and self.use_default is not None:
            _dict['use_default'] = self.use_default
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceVariableRequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceVariableRequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceVariableRequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class WorkspaceVariableResponse():
    """
    The description of your input variable.

    :attr str description: (optional) The description of your input variable.
    :attr str name: (optional) The name of the variable.
    :attr bool secure: (optional) If set to `true`, the value of your input variable
          is protected and not returned in your API response.
    :attr str type: (optional) `Terraform v0.11` supports `string`, `list`, `map`
          data type. For more information, about the syntax, see [Configuring input
          variables](https://www.terraform.io/docs/configuration-0-11/variables.html).
          <br> `Terraform v0.12` additionally, supports `bool`, `number` and complex data
          types such as `list(type)`, `map(type)`,
          `object({attribute name=type,..})`, `set(type)`, `tuple([type])`. For more
          information, about the syntax to use the complex data type, see [Configuring
          variables](https://www.terraform.io/docs/configuration/variables.html#type-constraints).
    :attr str value: (optional) Enter the value as a string for the primitive types
          such as `bool`, `number`, `string`, and `HCL` format for the complex variables,
          as you provide in a `.tfvars` file. **You need to enter escaped string of `HCL`
          format for the complex variable value**. For more information, about how to
          declare variables in a terraform configuration file and provide value to
          schematics, see [Providing values for the declared
          variables](https://cloud.ibm.com/docs/schematics?topic=schematics-create-tf-config#declare-variable).
    """

    def __init__(self,
                 *,
                 description: str = None,
                 name: str = None,
                 secure: bool = None,
                 type: str = None,
                 value: str = None) -> None:
        """
        Initialize a WorkspaceVariableResponse object.

        :param str description: (optional) The description of your input variable.
        :param str name: (optional) The name of the variable.
        :param bool secure: (optional) If set to `true`, the value of your input
               variable is protected and not returned in your API response.
        :param str type: (optional) `Terraform v0.11` supports `string`, `list`,
               `map` data type. For more information, about the syntax, see [Configuring
               input
               variables](https://www.terraform.io/docs/configuration-0-11/variables.html).
               <br> `Terraform v0.12` additionally, supports `bool`, `number` and complex
               data types such as `list(type)`, `map(type)`,
               `object({attribute name=type,..})`, `set(type)`, `tuple([type])`. For more
               information, about the syntax to use the complex data type, see
               [Configuring
               variables](https://www.terraform.io/docs/configuration/variables.html#type-constraints).
        :param str value: (optional) Enter the value as a string for the primitive
               types such as `bool`, `number`, `string`, and `HCL` format for the complex
               variables, as you provide in a `.tfvars` file. **You need to enter escaped
               string of `HCL` format for the complex variable value**. For more
               information, about how to declare variables in a terraform configuration
               file and provide value to schematics, see [Providing values for the
               declared
               variables](https://cloud.ibm.com/docs/schematics?topic=schematics-create-tf-config#declare-variable).
        """
        self.description = description
        self.name = name
        self.secure = secure
        self.type = type
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'WorkspaceVariableResponse':
        """Initialize a WorkspaceVariableResponse object from a json dictionary."""
        args = {}
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'secure' in _dict:
            args['secure'] = _dict.get('secure')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WorkspaceVariableResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'secure') and self.secure is not None:
            _dict['secure'] = self.secure
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this WorkspaceVariableResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'WorkspaceVariableResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'WorkspaceVariableResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other
