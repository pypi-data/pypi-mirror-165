'''
# cdktf

cdktf is a framework for defining cloud infrastructure using Terraform providers and modules. It allows for
users to define infrastructure resources using higher-level programming languages.

## Build

Install dependencies

```bash
yarn install
```

Build the package

```bash
yarn build
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import constructs


@jsii.enum(jsii_type="cdktf.AnnotationMetadataEntryType")
class AnnotationMetadataEntryType(enum.Enum):
    '''
    :stability: experimental
    '''

    INFO = "INFO"
    '''
    :stability: experimental
    '''
    WARN = "WARN"
    '''
    :stability: experimental
    '''
    ERROR = "ERROR"
    '''
    :stability: experimental
    '''


class Annotations(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Annotations"):
    '''(experimental) Includes API for attaching annotations such as warning messages to constructs.

    :stability: experimental
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, scope: constructs.IConstruct) -> "Annotations":
        '''(experimental) Returns the annotations API for a construct scope.

        :param scope: The scope.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Annotations.of)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("Annotations", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="addError")
    def add_error(self, message: builtins.str) -> None:
        '''(experimental) Adds an { "error":  } metadata entry to this construct.

        The toolkit will fail synthesis when errors are reported.

        :param message: The error message.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Annotations.add_error)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addError", [message]))

    @jsii.member(jsii_name="addInfo")
    def add_info(self, message: builtins.str) -> None:
        '''(experimental) Adds an info metadata entry to this construct.

        The CLI will display the info message when apps are synthesized.

        :param message: The info message.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Annotations.add_info)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addInfo", [message]))

    @jsii.member(jsii_name="addWarning")
    def add_warning(self, message: builtins.str) -> None:
        '''(experimental) Adds a warning metadata entry to this construct.

        The CLI will display the warning when an app is synthesized.
        In a future release the CLI might introduce a --strict flag which
        will then fail the synthesis if it encounters a warning.

        :param message: The warning message.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Annotations.add_warning)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addWarning", [message]))


class App(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.App"):
    '''(experimental) Represents a cdktf application.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        outdir: typing.Optional[builtins.str] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Defines an app.

        :param context: (experimental) Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdktf.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: (experimental) The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"
        :param skip_validation: (experimental) Whether to skip the validation during synthesis of the app. Default: - false
        :param stack_traces: 

        :stability: experimental
        '''
        options = AppOptions(
            context=context,
            outdir=outdir,
            skip_validation=skip_validation,
            stack_traces=stack_traces,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="isApp")
    @builtins.classmethod
    def is_app(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(App.is_app)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isApp", [x]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: constructs.IConstruct) -> "App":
        '''
        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(App.of)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast("App", jsii.sinvoke(cls, "of", [construct]))

    @jsii.member(jsii_name="crossStackReference")
    def cross_stack_reference(
        self,
        from_stack: "TerraformStack",
        to_stack: "TerraformStack",
        identifier: builtins.str,
    ) -> builtins.str:
        '''(experimental) Creates a reference from one stack to another, invoked on prepareStack since it creates extra resources.

        :param from_stack: -
        :param to_stack: -
        :param identifier: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(App.cross_stack_reference)
            check_type(argname="argument from_stack", value=from_stack, expected_type=type_hints["from_stack"])
            check_type(argname="argument to_stack", value=to_stack, expected_type=type_hints["to_stack"])
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
        return typing.cast(builtins.str, jsii.invoke(self, "crossStackReference", [from_stack, to_stack, identifier]))

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''(experimental) Synthesizes all resources to the output directory.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "Manifest":
        '''
        :stability: experimental
        '''
        return typing.cast("Manifest", jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''(experimental) The output directory into which resources will be synthesized.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to skip the validation during synthesis of the app.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipValidation"))

    @builtins.property
    @jsii.member(jsii_name="targetStackId")
    def target_stack_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The stack which will be synthesized.

        If not set, all stacks will be synthesized.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetStackId"))


@jsii.data_type(
    jsii_type="cdktf.AppOptions",
    jsii_struct_bases=[],
    name_mapping={
        "context": "context",
        "outdir": "outdir",
        "skip_validation": "skipValidation",
        "stack_traces": "stackTraces",
    },
)
class AppOptions:
    def __init__(
        self,
        *,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        outdir: typing.Optional[builtins.str] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param context: (experimental) Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdktf.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: (experimental) The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"
        :param skip_validation: (experimental) Whether to skip the validation during synthesis of the app. Default: - false
        :param stack_traces: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AppOptions.__init__)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument skip_validation", value=skip_validation, expected_type=type_hints["skip_validation"])
            check_type(argname="argument stack_traces", value=stack_traces, expected_type=type_hints["stack_traces"])
        self._values: typing.Dict[str, typing.Any] = {}
        if context is not None:
            self._values["context"] = context
        if outdir is not None:
            self._values["outdir"] = outdir
        if skip_validation is not None:
            self._values["skip_validation"] = skip_validation
        if stack_traces is not None:
            self._values["stack_traces"] = stack_traces

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional context values for the application.

        Context set by the CLI or the ``context`` key in ``cdktf.json`` has precedence.

        Context can be read from any construct using ``node.getContext(key)``.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory to output Terraform resources.

        :default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to skip the validation during synthesis of the app.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("skip_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stack_traces(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stack_traces")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.ArtifactoryBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "repo": "repo",
        "subpath": "subpath",
        "url": "url",
        "username": "username",
    },
)
class ArtifactoryBackendProps:
    def __init__(
        self,
        *,
        password: builtins.str,
        repo: builtins.str,
        subpath: builtins.str,
        url: builtins.str,
        username: builtins.str,
    ) -> None:
        '''(experimental) Stores the state as an artifact in a given repository in Artifactory.

        Generic HTTP repositories are supported, and state from different configurations
        may be kept at different subpaths within the repository.

        Note: The URL must include the path to the Artifactory installation.
        It will likely end in /artifactory.

        This backend does not support state locking.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/artifactory

        :param password: (experimental) (Required) - The password.
        :param repo: (experimental) (Required) - The repository name.
        :param subpath: (experimental) (Required) - Path within the repository.
        :param url: (experimental) (Required) - The URL. Note that this is the base url to artifactory not the full repo and subpath.
        :param username: (experimental) (Required) - The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ArtifactoryBackendProps.__init__)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument repo", value=repo, expected_type=type_hints["repo"])
            check_type(argname="argument subpath", value=subpath, expected_type=type_hints["subpath"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
            "repo": repo,
            "subpath": subpath,
            "url": url,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''(experimental) (Required) - The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo(self) -> builtins.str:
        '''(experimental) (Required) - The repository name.

        :stability: experimental
        '''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subpath(self) -> builtins.str:
        '''(experimental) (Required) - Path within the repository.

        :stability: experimental
        '''
        result = self._values.get("subpath")
        assert result is not None, "Required property 'subpath' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) (Required) - The URL.

        Note that this is the base url to artifactory not the full repo and subpath.

        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) (Required) - The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactoryBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Aspects(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Aspects"):
    '''(experimental) Aspects can be applied to CDK tree scopes and can operate on the tree before synthesis.

    :stability: experimental
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, scope: constructs.IConstruct) -> "Aspects":
        '''(experimental) Returns the ``Aspects`` object associated with a construct scope.

        :param scope: The scope for which these aspects will apply.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Aspects.of)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("Aspects", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="add")
    def add(self, aspect: "IAspect") -> None:
        '''(experimental) Adds an aspect to apply this scope before synthesis.

        :param aspect: The aspect to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Aspects.add)
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
        return typing.cast(None, jsii.invoke(self, "add", [aspect]))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.List["IAspect"]:
        '''(experimental) The list of aspects which were directly applied on this scope.

        :stability: experimental
        '''
        return typing.cast(typing.List["IAspect"], jsii.get(self, "all"))


@jsii.enum(jsii_type="cdktf.AssetType")
class AssetType(enum.Enum):
    '''
    :stability: experimental
    '''

    FILE = "FILE"
    '''
    :stability: experimental
    '''
    DIRECTORY = "DIRECTORY"
    '''
    :stability: experimental
    '''
    ARCHIVE = "ARCHIVE"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="cdktf.AzurermBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "key": "key",
        "storage_account_name": "storageAccountName",
        "access_key": "accessKey",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "endpoint": "endpoint",
        "environment": "environment",
        "msi_endpoint": "msiEndpoint",
        "resource_group_name": "resourceGroupName",
        "sas_token": "sasToken",
        "subscription_id": "subscriptionId",
        "tenant_id": "tenantId",
        "use_msi": "useMsi",
    },
)
class AzurermBackendProps:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        key: builtins.str,
        storage_account_name: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        msi_endpoint: typing.Optional[builtins.str] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        sas_token: typing.Optional[builtins.str] = None,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_msi: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Stores the state as a Blob with the given Key within the Blob Container within the Blob Storage Account.

        This backend supports state locking and consistency checking
        with Azure Blob Storage native capabilities.

        Note: By default the Azure Backend uses ADAL for authentication which is deprecated
        in favour of MSAL - MSAL can be used by setting use_microsoft_graph to true.
        The default for this will change in Terraform 1.2,
        so that MSAL authentication is used by default.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/azurerm

        :param container_name: (experimental) (Required) The Name of the Storage Container within the Storage Account.
        :param key: (experimental) (Required) The name of the Blob used to retrieve/store Terraform's State file inside the Storage Container.
        :param storage_account_name: (experimental) (Required) The Name of the Storage Account.
        :param access_key: (experimental) access_key - (Optional) The Access Key used to access the Blob Storage Account. This can also be sourced from the ARM_ACCESS_KEY environment variable.
        :param client_id: (experimental) (Optional) The Client ID of the Service Principal. This can also be sourced from the ARM_CLIENT_ID environment variable.
        :param client_secret: (experimental) (Optional) The Client Secret of the Service Principal. This can also be sourced from the ARM_CLIENT_SECRET environment variable.
        :param endpoint: (experimental) (Optional) The Custom Endpoint for Azure Resource Manager. This can also be sourced from the ARM_ENDPOINT environment variable. NOTE: An endpoint should only be configured when using Azure Stack.
        :param environment: (experimental) (Optional) The Azure Environment which should be used. This can also be sourced from the ARM_ENVIRONMENT environment variable. Possible values are public, china, german, stack and usgovernment. Defaults to public.
        :param msi_endpoint: (experimental) (Optional) The path to a custom Managed Service Identity endpoint which is automatically determined if not specified. This can also be sourced from the ARM_MSI_ENDPOINT environment variable.
        :param resource_group_name: (experimental) (Required) The Name of the Resource Group in which the Storage Account exists.
        :param sas_token: (experimental) (Optional) The SAS Token used to access the Blob Storage Account. This can also be sourced from the ARM_SAS_TOKEN environment variable.
        :param subscription_id: (experimental) (Optional) The Subscription ID in which the Storage Account exists. This can also be sourced from the ARM_SUBSCRIPTION_ID environment variable.
        :param tenant_id: (experimental) (Optional) The Tenant ID in which the Subscription exists. This can also be sourced from the ARM_TENANT_ID environment variable.
        :param use_msi: (experimental) (Optional) Should Managed Service Identity authentication be used? This can also be sourced from the ARM_USE_MSI environment variable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AzurermBackendProps.__init__)
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument storage_account_name", value=storage_account_name, expected_type=type_hints["storage_account_name"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument msi_endpoint", value=msi_endpoint, expected_type=type_hints["msi_endpoint"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sas_token", value=sas_token, expected_type=type_hints["sas_token"])
            check_type(argname="argument subscription_id", value=subscription_id, expected_type=type_hints["subscription_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument use_msi", value=use_msi, expected_type=type_hints["use_msi"])
        self._values: typing.Dict[str, typing.Any] = {
            "container_name": container_name,
            "key": key,
            "storage_account_name": storage_account_name,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if environment is not None:
            self._values["environment"] = environment
        if msi_endpoint is not None:
            self._values["msi_endpoint"] = msi_endpoint
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name
        if sas_token is not None:
            self._values["sas_token"] = sas_token
        if subscription_id is not None:
            self._values["subscription_id"] = subscription_id
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if use_msi is not None:
            self._values["use_msi"] = use_msi

    @builtins.property
    def container_name(self) -> builtins.str:
        '''(experimental) (Required) The Name of the Storage Container within the Storage Account.

        :stability: experimental
        '''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) (Required) The name of the Blob used to retrieve/store Terraform's State file inside the Storage Container.

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_name(self) -> builtins.str:
        '''(experimental) (Required) The Name of the Storage Account.

        :stability: experimental
        '''
        result = self._values.get("storage_account_name")
        assert result is not None, "Required property 'storage_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) access_key - (Optional) The Access Key used to access the Blob Storage Account.

        This can also be sourced from the ARM_ACCESS_KEY environment variable.

        :stability: experimental
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Client ID of the Service Principal.

        This can also be sourced from the ARM_CLIENT_ID environment variable.

        :stability: experimental
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Client Secret of the Service Principal.

        This can also be sourced from the ARM_CLIENT_SECRET environment variable.

        :stability: experimental
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Custom Endpoint for Azure Resource Manager. This can also be sourced from the ARM_ENDPOINT environment variable.

        NOTE: An endpoint should only be configured when using Azure Stack.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Azure Environment which should be used.

        This can also be sourced from the ARM_ENVIRONMENT environment variable.
        Possible values are public, china, german, stack and usgovernment. Defaults to public.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def msi_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to a custom Managed Service Identity endpoint which is automatically determined if not specified.

        This can also be sourced from the ARM_MSI_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("msi_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Required) The Name of the Resource Group in which the Storage Account exists.

        :stability: experimental
        '''
        result = self._values.get("resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sas_token(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The SAS Token used to access the Blob Storage Account.

        This can also be sourced from the ARM_SAS_TOKEN environment variable.

        :stability: experimental
        '''
        result = self._values.get("sas_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Subscription ID in which the Storage Account exists.

        This can also be sourced from the ARM_SUBSCRIPTION_ID environment variable.

        :stability: experimental
        '''
        result = self._values.get("subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Tenant ID in which the Subscription exists.

        This can also be sourced from the ARM_TENANT_ID environment variable.

        :stability: experimental
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_msi(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Should Managed Service Identity authentication be used?

        This can also be sourced from the ARM_USE_MSI environment variable.

        :stability: experimental
        '''
        result = self._values.get("use_msi")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.CloudBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "organization": "organization",
        "workspaces": "workspaces",
        "hostname": "hostname",
        "token": "token",
    },
)
class CloudBackendProps:
    def __init__(
        self,
        *,
        organization: builtins.str,
        workspaces: typing.Union["NamedCloudWorkspace", "TaggedCloudWorkspaces"],
        hostname: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The Cloud Backend synthesizes a {@link https://www.terraform.io/cli/cloud/settings#the-cloud-block cloud block}. The cloud block is a nested block within the top-level terraform settings block. It specifies which Terraform Cloud workspaces to use for the current working directory. The cloud block only affects Terraform CLI's behavior. When Terraform Cloud uses a configuration that contains a cloud block - for example, when a workspace is configured to use a VCS provider directly - it ignores the block and behaves according to its own workspace settings.

        https://www.terraform.io/cli/cloud/settings#arguments

        :param organization: (experimental) The name of the organization containing the workspace(s) the current configuration should use.
        :param workspaces: (experimental) A nested block that specifies which remote Terraform Cloud workspaces to use for the current configuration. The workspaces block must contain exactly one of the following arguments, each denoting a strategy for how workspaces should be mapped:
        :param hostname: (experimental) The hostname of a Terraform Enterprise installation, if using Terraform Enterprise. Default: app.terraform.io
        :param token: (experimental) The token used to authenticate with Terraform Cloud. We recommend omitting the token from the configuration, and instead using terraform login or manually configuring credentials in the CLI config file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudBackendProps.__init__)
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument workspaces", value=workspaces, expected_type=type_hints["workspaces"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[str, typing.Any] = {
            "organization": organization,
            "workspaces": workspaces,
        }
        if hostname is not None:
            self._values["hostname"] = hostname
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def organization(self) -> builtins.str:
        '''(experimental) The name of the organization containing the workspace(s) the current configuration should use.

        :stability: experimental
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspaces(
        self,
    ) -> typing.Union["NamedCloudWorkspace", "TaggedCloudWorkspaces"]:
        '''(experimental) A nested block that specifies which remote Terraform Cloud workspaces to use for the current configuration.

        The workspaces block must contain exactly one of the following arguments, each denoting a strategy for how workspaces should be mapped:

        :stability: experimental
        '''
        result = self._values.get("workspaces")
        assert result is not None, "Required property 'workspaces' is missing"
        return typing.cast(typing.Union["NamedCloudWorkspace", "TaggedCloudWorkspaces"], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hostname of a Terraform Enterprise installation, if using Terraform Enterprise.

        :default: app.terraform.io

        :stability: experimental
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) The token used to authenticate with Terraform Cloud.

        We recommend omitting the token from the configuration, and instead using terraform login or manually configuring credentials in the CLI config file.

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudWorkspace(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.CloudWorkspace",
):
    '''(experimental) A cloud workspace can either be a single named workspace, or a list of tagged workspaces.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toTerraform")
    @abc.abstractmethod
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        ...


class _CloudWorkspaceProxy(CloudWorkspace):
    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, CloudWorkspace).__jsii_proxy_class__ = lambda : _CloudWorkspaceProxy


@jsii.data_type(
    jsii_type="cdktf.ConsulBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "path": "path",
        "address": "address",
        "ca_file": "caFile",
        "cert_file": "certFile",
        "datacenter": "datacenter",
        "gzip": "gzip",
        "http_auth": "httpAuth",
        "key_file": "keyFile",
        "lock": "lock",
        "scheme": "scheme",
    },
)
class ConsulBackendProps:
    def __init__(
        self,
        *,
        access_token: builtins.str,
        path: builtins.str,
        address: typing.Optional[builtins.str] = None,
        ca_file: typing.Optional[builtins.str] = None,
        cert_file: typing.Optional[builtins.str] = None,
        datacenter: typing.Optional[builtins.str] = None,
        gzip: typing.Optional[builtins.bool] = None,
        http_auth: typing.Optional[builtins.str] = None,
        key_file: typing.Optional[builtins.str] = None,
        lock: typing.Optional[builtins.bool] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Stores the state in the Consul KV store at a given path. This backend supports state locking.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/consul

        :param access_token: (experimental) (Required) Access token.
        :param path: (experimental) (Required) Path in the Consul KV store.
        :param address: (experimental) (Optional) DNS name and port of your Consul endpoint specified in the format dnsname:port. Defaults to the local agent HTTP listener.
        :param ca_file: (experimental) (Optional) A path to a PEM-encoded certificate authority used to verify the remote agent's certificate.
        :param cert_file: (experimental) (Optional) A path to a PEM-encoded certificate provided to the remote agent; requires use of key_file.
        :param datacenter: (experimental) (Optional) The datacenter to use. Defaults to that of the agent.
        :param gzip: (experimental) (Optional) true to compress the state data using gzip, or false (the default) to leave it uncompressed.
        :param http_auth: (experimental) (Optional) HTTP Basic Authentication credentials to be used when communicating with Consul, in the format of either user or user:pass.
        :param key_file: (experimental) (Optional) A path to a PEM-encoded private key, required if cert_file is specified.
        :param lock: (experimental) (Optional) false to disable locking. This defaults to true, but will require session permissions with Consul and at least kv write permissions on $path/.lock to perform locking.
        :param scheme: (experimental) (Optional) Specifies what protocol to use when talking to the given address,either http or https. SSL support can also be triggered by setting then environment variable CONSUL_HTTP_SSL to true.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ConsulBackendProps.__init__)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument ca_file", value=ca_file, expected_type=type_hints["ca_file"])
            check_type(argname="argument cert_file", value=cert_file, expected_type=type_hints["cert_file"])
            check_type(argname="argument datacenter", value=datacenter, expected_type=type_hints["datacenter"])
            check_type(argname="argument gzip", value=gzip, expected_type=type_hints["gzip"])
            check_type(argname="argument http_auth", value=http_auth, expected_type=type_hints["http_auth"])
            check_type(argname="argument key_file", value=key_file, expected_type=type_hints["key_file"])
            check_type(argname="argument lock", value=lock, expected_type=type_hints["lock"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[str, typing.Any] = {
            "access_token": access_token,
            "path": path,
        }
        if address is not None:
            self._values["address"] = address
        if ca_file is not None:
            self._values["ca_file"] = ca_file
        if cert_file is not None:
            self._values["cert_file"] = cert_file
        if datacenter is not None:
            self._values["datacenter"] = datacenter
        if gzip is not None:
            self._values["gzip"] = gzip
        if http_auth is not None:
            self._values["http_auth"] = http_auth
        if key_file is not None:
            self._values["key_file"] = key_file
        if lock is not None:
            self._values["lock"] = lock
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def access_token(self) -> builtins.str:
        '''(experimental) (Required) Access token.

        :stability: experimental
        '''
        result = self._values.get("access_token")
        assert result is not None, "Required property 'access_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) (Required) Path in the Consul KV store.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) DNS name and port of your Consul endpoint specified in the format dnsname:port.

        Defaults to the local agent HTTP listener.

        :stability: experimental
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A path to a PEM-encoded certificate authority used to verify the remote agent's certificate.

        :stability: experimental
        '''
        result = self._values.get("ca_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A path to a PEM-encoded certificate provided to the remote agent;

        requires use of key_file.

        :stability: experimental
        '''
        result = self._values.get("cert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datacenter(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The datacenter to use.

        Defaults to that of the agent.

        :stability: experimental
        '''
        result = self._values.get("datacenter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gzip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) true to compress the state data using gzip, or false (the default) to leave it uncompressed.

        :stability: experimental
        '''
        result = self._values.get("gzip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def http_auth(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) HTTP Basic Authentication credentials to be used when communicating with Consul, in the format of either user or user:pass.

        :stability: experimental
        '''
        result = self._values.get("http_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A path to a PEM-encoded private key, required if cert_file is specified.

        :stability: experimental
        '''
        result = self._values.get("key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) false to disable locking.

        This defaults to true, but will require session permissions with Consul and
        at least kv write permissions on $path/.lock to perform locking.

        :stability: experimental
        '''
        result = self._values.get("lock")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Specifies what protocol to use when talking to the given address,either http or https.

        SSL support can also be triggered by setting then environment variable CONSUL_HTTP_SSL to true.

        :stability: experimental
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConsulBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.CosBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "acl": "acl",
        "encrypt": "encrypt",
        "key": "key",
        "prefix": "prefix",
        "region": "region",
        "secret_id": "secretId",
        "secret_key": "secretKey",
    },
)
class CosBackendProps:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_id: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Stores the state as an object in a configurable prefix in a given bucket on Tencent Cloud Object Storage (COS).

        This backend supports state locking.

        Warning! It is highly recommended that you enable Object Versioning on the COS bucket to allow for state recovery in the case of accidental deletions and human error.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/cos

        :param bucket: (experimental) (Required) The name of the COS bucket. You shall manually create it first.
        :param acl: (experimental) (Optional) Object ACL to be applied to the state file, allows private and public-read. Defaults to private.
        :param encrypt: (experimental) (Optional) Whether to enable server side encryption of the state file. If it is true, COS will use 'AES256' encryption algorithm to encrypt state file.
        :param key: (experimental) (Optional) The path for saving the state file in bucket. Defaults to terraform.tfstate.
        :param prefix: (experimental) (Optional) The directory for saving the state file in bucket. Default to "env:".
        :param region: (experimental) (Optional) The region of the COS bucket. It supports environment variables TENCENTCLOUD_REGION.
        :param secret_id: (experimental) (Optional) Secret id of Tencent Cloud. It supports environment variables TENCENTCLOUD_SECRET_ID.
        :param secret_key: (experimental) (Optional) Secret key of Tencent Cloud. It supports environment variables TENCENTCLOUD_SECRET_KEY.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CosBackendProps.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument encrypt", value=encrypt, expected_type=type_hints["encrypt"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if acl is not None:
            self._values["acl"] = acl
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix
        if region is not None:
            self._values["region"] = region
        if secret_id is not None:
            self._values["secret_id"] = secret_id
        if secret_key is not None:
            self._values["secret_key"] = secret_key

    @builtins.property
    def bucket(self) -> builtins.str:
        '''(experimental) (Required) The name of the COS bucket.

        You shall manually create it first.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Object ACL to be applied to the state file, allows private and public-read.

        Defaults to private.

        :stability: experimental
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypt(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Whether to enable server side encryption of the state file.

        If it is true, COS will use 'AES256' encryption algorithm to encrypt state file.

        :stability: experimental
        '''
        result = self._values.get("encrypt")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path for saving the state file in bucket.

        Defaults to terraform.tfstate.

        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The directory for saving the state file in bucket.

        Default to "env:".

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The region of the COS bucket.

        It supports environment variables TENCENTCLOUD_REGION.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Secret id of Tencent Cloud.

        It supports environment variables TENCENTCLOUD_SECRET_ID.

        :stability: experimental
        '''
        result = self._values.get("secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Secret key of Tencent Cloud.

        It supports environment variables TENCENTCLOUD_SECRET_KEY.

        :stability: experimental
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateConfig",
    jsii_struct_bases=[],
    name_mapping={"defaults": "defaults", "workspace": "workspace"},
)
class DataTerraformRemoteStateConfig:
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
        self._values: typing.Dict[str, typing.Any] = {}
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateConsulConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, ConsulBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "access_token": "accessToken",
        "path": "path",
        "address": "address",
        "ca_file": "caFile",
        "cert_file": "certFile",
        "datacenter": "datacenter",
        "gzip": "gzip",
        "http_auth": "httpAuth",
        "key_file": "keyFile",
        "lock": "lock",
        "scheme": "scheme",
    },
)
class DataTerraformRemoteStateConsulConfig(
    DataTerraformRemoteStateConfig,
    ConsulBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        access_token: builtins.str,
        path: builtins.str,
        address: typing.Optional[builtins.str] = None,
        ca_file: typing.Optional[builtins.str] = None,
        cert_file: typing.Optional[builtins.str] = None,
        datacenter: typing.Optional[builtins.str] = None,
        gzip: typing.Optional[builtins.bool] = None,
        http_auth: typing.Optional[builtins.str] = None,
        key_file: typing.Optional[builtins.str] = None,
        lock: typing.Optional[builtins.bool] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param access_token: (experimental) (Required) Access token.
        :param path: (experimental) (Required) Path in the Consul KV store.
        :param address: (experimental) (Optional) DNS name and port of your Consul endpoint specified in the format dnsname:port. Defaults to the local agent HTTP listener.
        :param ca_file: (experimental) (Optional) A path to a PEM-encoded certificate authority used to verify the remote agent's certificate.
        :param cert_file: (experimental) (Optional) A path to a PEM-encoded certificate provided to the remote agent; requires use of key_file.
        :param datacenter: (experimental) (Optional) The datacenter to use. Defaults to that of the agent.
        :param gzip: (experimental) (Optional) true to compress the state data using gzip, or false (the default) to leave it uncompressed.
        :param http_auth: (experimental) (Optional) HTTP Basic Authentication credentials to be used when communicating with Consul, in the format of either user or user:pass.
        :param key_file: (experimental) (Optional) A path to a PEM-encoded private key, required if cert_file is specified.
        :param lock: (experimental) (Optional) false to disable locking. This defaults to true, but will require session permissions with Consul and at least kv write permissions on $path/.lock to perform locking.
        :param scheme: (experimental) (Optional) Specifies what protocol to use when talking to the given address,either http or https. SSL support can also be triggered by setting then environment variable CONSUL_HTTP_SSL to true.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateConsulConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument ca_file", value=ca_file, expected_type=type_hints["ca_file"])
            check_type(argname="argument cert_file", value=cert_file, expected_type=type_hints["cert_file"])
            check_type(argname="argument datacenter", value=datacenter, expected_type=type_hints["datacenter"])
            check_type(argname="argument gzip", value=gzip, expected_type=type_hints["gzip"])
            check_type(argname="argument http_auth", value=http_auth, expected_type=type_hints["http_auth"])
            check_type(argname="argument key_file", value=key_file, expected_type=type_hints["key_file"])
            check_type(argname="argument lock", value=lock, expected_type=type_hints["lock"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[str, typing.Any] = {
            "access_token": access_token,
            "path": path,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if address is not None:
            self._values["address"] = address
        if ca_file is not None:
            self._values["ca_file"] = ca_file
        if cert_file is not None:
            self._values["cert_file"] = cert_file
        if datacenter is not None:
            self._values["datacenter"] = datacenter
        if gzip is not None:
            self._values["gzip"] = gzip
        if http_auth is not None:
            self._values["http_auth"] = http_auth
        if key_file is not None:
            self._values["key_file"] = key_file
        if lock is not None:
            self._values["lock"] = lock
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_token(self) -> builtins.str:
        '''(experimental) (Required) Access token.

        :stability: experimental
        '''
        result = self._values.get("access_token")
        assert result is not None, "Required property 'access_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) (Required) Path in the Consul KV store.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) DNS name and port of your Consul endpoint specified in the format dnsname:port.

        Defaults to the local agent HTTP listener.

        :stability: experimental
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A path to a PEM-encoded certificate authority used to verify the remote agent's certificate.

        :stability: experimental
        '''
        result = self._values.get("ca_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A path to a PEM-encoded certificate provided to the remote agent;

        requires use of key_file.

        :stability: experimental
        '''
        result = self._values.get("cert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datacenter(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The datacenter to use.

        Defaults to that of the agent.

        :stability: experimental
        '''
        result = self._values.get("datacenter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gzip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) true to compress the state data using gzip, or false (the default) to leave it uncompressed.

        :stability: experimental
        '''
        result = self._values.get("gzip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def http_auth(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) HTTP Basic Authentication credentials to be used when communicating with Consul, in the format of either user or user:pass.

        :stability: experimental
        '''
        result = self._values.get("http_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A path to a PEM-encoded private key, required if cert_file is specified.

        :stability: experimental
        '''
        result = self._values.get("key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) false to disable locking.

        This defaults to true, but will require session permissions with Consul and
        at least kv write permissions on $path/.lock to perform locking.

        :stability: experimental
        '''
        result = self._values.get("lock")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Specifies what protocol to use when talking to the given address,either http or https.

        SSL support can also be triggered by setting then environment variable CONSUL_HTTP_SSL to true.

        :stability: experimental
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateConsulConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateCosConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, CosBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "bucket": "bucket",
        "acl": "acl",
        "encrypt": "encrypt",
        "key": "key",
        "prefix": "prefix",
        "region": "region",
        "secret_id": "secretId",
        "secret_key": "secretKey",
    },
)
class DataTerraformRemoteStateCosConfig(
    DataTerraformRemoteStateConfig,
    CosBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        bucket: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_id: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param bucket: (experimental) (Required) The name of the COS bucket. You shall manually create it first.
        :param acl: (experimental) (Optional) Object ACL to be applied to the state file, allows private and public-read. Defaults to private.
        :param encrypt: (experimental) (Optional) Whether to enable server side encryption of the state file. If it is true, COS will use 'AES256' encryption algorithm to encrypt state file.
        :param key: (experimental) (Optional) The path for saving the state file in bucket. Defaults to terraform.tfstate.
        :param prefix: (experimental) (Optional) The directory for saving the state file in bucket. Default to "env:".
        :param region: (experimental) (Optional) The region of the COS bucket. It supports environment variables TENCENTCLOUD_REGION.
        :param secret_id: (experimental) (Optional) Secret id of Tencent Cloud. It supports environment variables TENCENTCLOUD_SECRET_ID.
        :param secret_key: (experimental) (Optional) Secret key of Tencent Cloud. It supports environment variables TENCENTCLOUD_SECRET_KEY.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateCosConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument encrypt", value=encrypt, expected_type=type_hints["encrypt"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if acl is not None:
            self._values["acl"] = acl
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix
        if region is not None:
            self._values["region"] = region
        if secret_id is not None:
            self._values["secret_id"] = secret_id
        if secret_key is not None:
            self._values["secret_key"] = secret_key

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> builtins.str:
        '''(experimental) (Required) The name of the COS bucket.

        You shall manually create it first.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Object ACL to be applied to the state file, allows private and public-read.

        Defaults to private.

        :stability: experimental
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypt(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Whether to enable server side encryption of the state file.

        If it is true, COS will use 'AES256' encryption algorithm to encrypt state file.

        :stability: experimental
        '''
        result = self._values.get("encrypt")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path for saving the state file in bucket.

        Defaults to terraform.tfstate.

        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The directory for saving the state file in bucket.

        Default to "env:".

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The region of the COS bucket.

        It supports environment variables TENCENTCLOUD_REGION.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Secret id of Tencent Cloud.

        It supports environment variables TENCENTCLOUD_SECRET_ID.

        :stability: experimental
        '''
        result = self._values.get("secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Secret key of Tencent Cloud.

        It supports environment variables TENCENTCLOUD_SECRET_KEY.

        :stability: experimental
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateCosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.EncodingOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint"},
)
class EncodingOptions:
    def __init__(self, *, display_hint: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Properties to string encodings.

        :param display_hint: (experimental) A hint for the Token's purpose when stringifying it. Default: - no display hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EncodingOptions.__init__)
            check_type(argname="argument display_hint", value=display_hint, expected_type=type_hints["display_hint"])
        self._values: typing.Dict[str, typing.Any] = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[builtins.str]:
        '''(experimental) A hint for the Token's purpose when stringifying it.

        :default: - no display hint

        :stability: experimental
        '''
        result = self._values.get("display_hint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncodingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.EtcdBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoints": "endpoints",
        "path": "path",
        "password": "password",
        "username": "username",
    },
)
class EtcdBackendProps:
    def __init__(
        self,
        *,
        endpoints: builtins.str,
        path: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Stores the state in etcd 2.x at a given path.

        This backend does not support state locking.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/etcd

        :param endpoints: (experimental) (Required) A space-separated list of the etcd endpoints.
        :param path: (experimental) (Required) The path where to store the state.
        :param password: (experimental) (Optional) The password.
        :param username: (experimental) (Optional) The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EtcdBackendProps.__init__)
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "endpoints": endpoints,
            "path": path,
        }
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def endpoints(self) -> builtins.str:
        '''(experimental) (Required) A space-separated list of the etcd endpoints.

        :stability: experimental
        '''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) (Required) The path where to store the state.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EtcdBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.EtcdV3BackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoints": "endpoints",
        "cacert_path": "cacertPath",
        "cert_path": "certPath",
        "key_path": "keyPath",
        "lock": "lock",
        "password": "password",
        "prefix": "prefix",
        "username": "username",
    },
)
class EtcdV3BackendProps:
    def __init__(
        self,
        *,
        endpoints: typing.Sequence[builtins.str],
        cacert_path: typing.Optional[builtins.str] = None,
        cert_path: typing.Optional[builtins.str] = None,
        key_path: typing.Optional[builtins.str] = None,
        lock: typing.Optional[builtins.bool] = None,
        password: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Stores the state in the etcd KV store with a given prefix.

        This backend supports state locking.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/etcdv3

        :param endpoints: (experimental) (Required) The list of 'etcd' endpoints which to connect to.
        :param cacert_path: (experimental) (Optional) The path to a PEM-encoded CA bundle with which to verify certificates of TLS-enabled etcd servers.
        :param cert_path: (experimental) (Optional) The path to a PEM-encoded certificate to provide to etcd for secure client identification.
        :param key_path: (experimental) (Optional) The path to a PEM-encoded key to provide to etcd for secure client identification.
        :param lock: (experimental) (Optional) Whether to lock state access. Defaults to true.
        :param password: (experimental) (Optional) Password used to connect to the etcd cluster.
        :param prefix: (experimental) (Optional) An optional prefix to be added to keys when to storing state in etcd. Defaults to "".
        :param username: (experimental) (Optional) Username used to connect to the etcd cluster.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EtcdV3BackendProps.__init__)
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument cacert_path", value=cacert_path, expected_type=type_hints["cacert_path"])
            check_type(argname="argument cert_path", value=cert_path, expected_type=type_hints["cert_path"])
            check_type(argname="argument key_path", value=key_path, expected_type=type_hints["key_path"])
            check_type(argname="argument lock", value=lock, expected_type=type_hints["lock"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "endpoints": endpoints,
        }
        if cacert_path is not None:
            self._values["cacert_path"] = cacert_path
        if cert_path is not None:
            self._values["cert_path"] = cert_path
        if key_path is not None:
            self._values["key_path"] = key_path
        if lock is not None:
            self._values["lock"] = lock
        if password is not None:
            self._values["password"] = password
        if prefix is not None:
            self._values["prefix"] = prefix
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def endpoints(self) -> typing.List[builtins.str]:
        '''(experimental) (Required) The list of 'etcd' endpoints which to connect to.

        :stability: experimental
        '''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cacert_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to a PEM-encoded CA bundle with which to verify certificates of TLS-enabled etcd servers.

        :stability: experimental
        '''
        result = self._values.get("cacert_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to a PEM-encoded certificate to provide to etcd for secure client identification.

        :stability: experimental
        '''
        result = self._values.get("cert_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to a PEM-encoded key to provide to etcd for secure client identification.

        :stability: experimental
        '''
        result = self._values.get("key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Whether to lock state access.

        Defaults to true.

        :stability: experimental
        '''
        result = self._values.get("lock")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Password used to connect to the etcd cluster.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) An optional prefix to be added to keys when to storing state in etcd.

        Defaults to "".

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Username used to connect to the etcd cluster.

        :stability: experimental
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EtcdV3BackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.FileProvisioner",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "type": "type",
        "connection": "connection",
        "content": "content",
        "source": "source",
    },
)
class FileProvisioner:
    def __init__(
        self,
        *,
        destination: builtins.str,
        type: builtins.str,
        connection: typing.Optional[typing.Union[typing.Union["SSHProvisionerConnection", typing.Dict[str, typing.Any]], typing.Union["WinrmProvisionerConnection", typing.Dict[str, typing.Any]]]] = None,
        content: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The file provisioner copies files or directories from the machine running Terraform to the newly created resource.

        The file provisioner supports both ssh and winrm type connections.

        See {@link https://www.terraform.io/language/resources/provisioners/file file}

        :param destination: (experimental) The source file or directory. Specify it either relative to the current working directory or as an absolute path. This argument cannot be combined with content.
        :param type: 
        :param connection: (experimental) Most provisioners require access to the remote resource via SSH or WinRM and expect a nested connection block with details about how to connect.
        :param content: (experimental) The destination path to write to on the remote system. See Destination Paths below for more information.
        :param source: (experimental) The direct content to copy on the destination. If destination is a file, the content will be written on that file. In case of a directory, a file named tf-file-content is created inside that directory. We recommend using a file as the destination when using content. This argument cannot be combined with source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FileProvisioner.__init__)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[str, typing.Any] = {
            "destination": destination,
            "type": type,
        }
        if connection is not None:
            self._values["connection"] = connection
        if content is not None:
            self._values["content"] = content
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def destination(self) -> builtins.str:
        '''(experimental) The source file or directory.

        Specify it either relative to the current working directory or as an absolute path.
        This argument cannot be combined with content.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union["SSHProvisionerConnection", "WinrmProvisionerConnection"]]:
        '''(experimental) Most provisioners require access to the remote resource via SSH or WinRM and expect a nested connection block with details about how to connect.

        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union["SSHProvisionerConnection", "WinrmProvisionerConnection"]], result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''(experimental) The destination path to write to on the remote system.

        See Destination Paths below for more information.

        :stability: experimental
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''(experimental) The direct content to copy on the destination.

        If destination is a file, the content will be written on that file.
        In case of a directory, a file named tf-file-content is created inside that directory.
        We recommend using a file as the destination when using content.
        This argument cannot be combined with source.

        :stability: experimental
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileProvisioner(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Fn(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Fn"):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="abs")
    @builtins.classmethod
    def abs(cls, value: jsii.Number) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/abs.html abs} returns the absolute value of the given number.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.abs)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "abs", [value]))

    @jsii.member(jsii_name="abspath")
    @builtins.classmethod
    def abspath(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/abspath.html abspath} takes a string containing a filesystem path and converts it to an absolute path.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.abspath)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "abspath", [value]))

    @jsii.member(jsii_name="alltrue")
    @builtins.classmethod
    def alltrue(cls, values: typing.Sequence[typing.Any]) -> "IResolvable":
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/alltrue.html alltrue} returns true if all elements in a given collection are true or "true".

        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.alltrue)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast("IResolvable", jsii.sinvoke(cls, "alltrue", [values]))

    @jsii.member(jsii_name="anytrue")
    @builtins.classmethod
    def anytrue(cls, value: typing.Sequence[typing.Any]) -> "IResolvable":
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/anytrue.html anytrue} returns true if any element in a given collection is true or "true".

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.anytrue)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("IResolvable", jsii.sinvoke(cls, "anytrue", [value]))

    @jsii.member(jsii_name="base64decode")
    @builtins.classmethod
    def base64decode(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/base64decode.html base64decode} takes a string containing a Base64 character sequence and returns the original string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.base64decode)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "base64decode", [value]))

    @jsii.member(jsii_name="base64encode")
    @builtins.classmethod
    def base64encode(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/base64encode.html base64encode} takes a string containing a Base64 character sequence and returns the original string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.base64encode)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "base64encode", [value]))

    @jsii.member(jsii_name="base64gzip")
    @builtins.classmethod
    def base64gzip(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/base64gzip.html base64gzip} compresses a string with gzip and then encodes the result in Base64 encoding.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.base64gzip)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "base64gzip", [value]))

    @jsii.member(jsii_name="base64sha256")
    @builtins.classmethod
    def base64sha256(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/base64sha256.html base64sha256} computes the SHA256 hash of a given string and encodes it with Base64.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.base64sha256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "base64sha256", [value]))

    @jsii.member(jsii_name="base64sha512")
    @builtins.classmethod
    def base64sha512(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/base64sha512.html base64sha512} computes the SHA512 hash of a given string and encodes it with Base64.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.base64sha512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "base64sha512", [value]))

    @jsii.member(jsii_name="basename")
    @builtins.classmethod
    def basename(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/basename.html basename} takes a string containing a filesystem path and removes all except the last portion from it.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.basename)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "basename", [value]))

    @jsii.member(jsii_name="bcrypt")
    @builtins.classmethod
    def bcrypt(
        cls,
        value: builtins.str,
        cost: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/bcrypt.html bcrypt} computes a hash of the given string using the Blowfish cipher, returning a string in the Modular Crypt Format usually expected in the shadow password file on many Unix systems.

        :param value: -
        :param cost: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.bcrypt)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument cost", value=cost, expected_type=type_hints["cost"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "bcrypt", [value, cost]))

    @jsii.member(jsii_name="can")
    @builtins.classmethod
    def can(cls, expression: typing.Any) -> "IResolvable":
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/can.html can} evaluates the given expression and returns a boolean value indicating whether the expression produced a result without any errors.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.can)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast("IResolvable", jsii.sinvoke(cls, "can", [expression]))

    @jsii.member(jsii_name="ceil")
    @builtins.classmethod
    def ceil(cls, value: jsii.Number) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/ceil.html ceil} returns the closest whole number that is greater than or equal to the given value, which may be a fraction.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.ceil)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "ceil", [value]))

    @jsii.member(jsii_name="chomp")
    @builtins.classmethod
    def chomp(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/chomp.html chomp} removes newline characters at the end of a string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.chomp)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "chomp", [value]))

    @jsii.member(jsii_name="chunklist")
    @builtins.classmethod
    def chunklist(
        cls,
        value: typing.Sequence[typing.Any],
        chunk_size: jsii.Number,
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/chunklist.html chunklist} splits a single list into fixed-size chunks, returning a list of lists.

        :param value: -
        :param chunk_size: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.chunklist)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument chunk_size", value=chunk_size, expected_type=type_hints["chunk_size"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "chunklist", [value, chunk_size]))

    @jsii.member(jsii_name="cidrhost")
    @builtins.classmethod
    def cidrhost(cls, prefix: builtins.str, hostnum: jsii.Number) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/cidrhost.html cidrhost} calculates a full host IP address for a given host number within a given IP network address prefix.

        :param prefix: -
        :param hostnum: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.cidrhost)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument hostnum", value=hostnum, expected_type=type_hints["hostnum"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "cidrhost", [prefix, hostnum]))

    @jsii.member(jsii_name="cidrnetmask")
    @builtins.classmethod
    def cidrnetmask(cls, prefix: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/cidrnetmask.html cidrnetmask} converts an IPv4 address prefix given in CIDR notation into a subnet mask address.

        :param prefix: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.cidrnetmask)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "cidrnetmask", [prefix]))

    @jsii.member(jsii_name="cidrsubnet")
    @builtins.classmethod
    def cidrsubnet(
        cls,
        prefix: builtins.str,
        newbits: jsii.Number,
        netnum: jsii.Number,
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/cidrsubnet.html cidrsubnet} calculates a subnet address within given IP network address prefix.

        :param prefix: -
        :param newbits: -
        :param netnum: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.cidrsubnet)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument newbits", value=newbits, expected_type=type_hints["newbits"])
            check_type(argname="argument netnum", value=netnum, expected_type=type_hints["netnum"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "cidrsubnet", [prefix, newbits, netnum]))

    @jsii.member(jsii_name="cidrsubnets")
    @builtins.classmethod
    def cidrsubnets(
        cls,
        prefix: builtins.str,
        newbits: typing.Sequence[jsii.Number],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/cidrsubnets.html cidrsubnets} calculates a sequence of consecutive IP address ranges within a particular CIDR prefix.

        :param prefix: -
        :param newbits: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.cidrsubnets)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument newbits", value=newbits, expected_type=type_hints["newbits"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "cidrsubnets", [prefix, newbits]))

    @jsii.member(jsii_name="coalesce")
    @builtins.classmethod
    def coalesce(cls, value: typing.Sequence[typing.Any]) -> "IResolvable":
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/coalesce.html coalesce} takes any number of arguments and returns the first one that isn't null or an empty string.

        :param value: - Arguments are passed in an array.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.coalesce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("IResolvable", jsii.sinvoke(cls, "coalesce", [value]))

    @jsii.member(jsii_name="coalescelist")
    @builtins.classmethod
    def coalescelist(
        cls,
        value: typing.Sequence[typing.Sequence[typing.Any]],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/coalescelist.html coalescelist} takes any number of list arguments and returns the first one that isn't empty.

        :param value: - Arguments are passed in an array.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.coalescelist)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "coalescelist", [value]))

    @jsii.member(jsii_name="compact")
    @builtins.classmethod
    def compact(cls, value: typing.Sequence[builtins.str]) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/compact.html compact} takes a list of strings and returns a new list with any empty string elements removed.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.compact)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "compact", [value]))

    @jsii.member(jsii_name="concat")
    @builtins.classmethod
    def concat(
        cls,
        value: typing.Sequence[typing.Sequence[typing.Any]],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/concat.html concat} takes two or more lists and combines them into a single list.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.concat)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "concat", [value]))

    @jsii.member(jsii_name="contains")
    @builtins.classmethod
    def contains(
        cls,
        list: typing.Union[typing.Sequence[typing.Any], "IResolvable"],
        value: typing.Any,
    ) -> "IResolvable":
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/contains.html contains} determines whether a given list or set contains a given single value as one of its elements.

        :param list: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.contains)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("IResolvable", jsii.sinvoke(cls, "contains", [list, value]))

    @jsii.member(jsii_name="csvdecode")
    @builtins.classmethod
    def csvdecode(cls, value: builtins.str) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/csvdecode.html csvdecode} decodes a string containing CSV-formatted data and produces a list of maps representing that data.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.csvdecode)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "csvdecode", [value]))

    @jsii.member(jsii_name="dirname")
    @builtins.classmethod
    def dirname(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/dirname.html dirname} takes a string containing a filesystem path and removes the last portion from it.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.dirname)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "dirname", [value]))

    @jsii.member(jsii_name="distinct")
    @builtins.classmethod
    def distinct(
        cls,
        list: typing.Union[typing.Sequence[typing.Any], "IResolvable"],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/distinct.html distinct} takes a list and returns a new list with any duplicate elements removed.

        :param list: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.distinct)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "distinct", [list]))

    @jsii.member(jsii_name="element")
    @builtins.classmethod
    def element(
        cls,
        list: typing.Union[typing.Sequence[typing.Any], "IResolvable"],
        index: jsii.Number,
    ) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/element.html element} retrieves a single element from a list.

        :param list: -
        :param index: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.element)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "element", [list, index]))

    @jsii.member(jsii_name="file")
    @builtins.classmethod
    def file(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/file.html file} takes a string containing a filesystem path and removes all except the last portion from it.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.file)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "file", [value]))

    @jsii.member(jsii_name="filebase64")
    @builtins.classmethod
    def filebase64(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/filebase64.html filebase64} reads the contents of a file at the given path and returns them as a base64-encoded string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.filebase64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "filebase64", [value]))

    @jsii.member(jsii_name="filebase64sha256")
    @builtins.classmethod
    def filebase64sha256(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/filebase64sha256.html filebase64sha256} is a variant of base64sha256 that hashes the contents of a given file rather than a literal string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.filebase64sha256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "filebase64sha256", [value]))

    @jsii.member(jsii_name="filebase64sha512")
    @builtins.classmethod
    def filebase64sha512(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/filebase64sha512.html filebase64sha512} is a variant of base64sha512 that hashes the contents of a given file rather than a literal string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.filebase64sha512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "filebase64sha512", [value]))

    @jsii.member(jsii_name="fileexists")
    @builtins.classmethod
    def fileexists(cls, value: builtins.str) -> "IResolvable":
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/fileexists.html fileexists} determines whether a file exists at a given path.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.fileexists)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("IResolvable", jsii.sinvoke(cls, "fileexists", [value]))

    @jsii.member(jsii_name="filemd5")
    @builtins.classmethod
    def filemd5(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/filemd5.html filemd5} is a variant of md5 that hashes the contents of a given file rather than a literal string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.filemd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "filemd5", [value]))

    @jsii.member(jsii_name="fileset")
    @builtins.classmethod
    def fileset(
        cls,
        path: builtins.str,
        pattern: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/fileset.html fileset} enumerates a set of regular file names given a path and pattern.

        :param path: -
        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.fileset)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "fileset", [path, pattern]))

    @jsii.member(jsii_name="filesha1")
    @builtins.classmethod
    def filesha1(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/filesha1.html filesha1} is a variant of sha1 that hashes the contents of a given file rather than a literal string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.filesha1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "filesha1", [value]))

    @jsii.member(jsii_name="filesha256")
    @builtins.classmethod
    def filesha256(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/filesha256.html filesha256} is a variant of sha256 that hashes the contents of a given file rather than a literal string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.filesha256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "filesha256", [value]))

    @jsii.member(jsii_name="filesha512")
    @builtins.classmethod
    def filesha512(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/filesha512.html filesha512} is a variant of sha512 that hashes the contents of a given file rather than a literal string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.filesha512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "filesha512", [value]))

    @jsii.member(jsii_name="flatten")
    @builtins.classmethod
    def flatten(
        cls,
        list: typing.Union[typing.Sequence[typing.Any], "IResolvable"],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/flatten.html flatten} takes a list and replaces any elements that are lists with a flattened sequence of the list contents.

        :param list: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.flatten)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "flatten", [list]))

    @jsii.member(jsii_name="floor")
    @builtins.classmethod
    def floor(cls, value: jsii.Number) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/floor.html floor} returns the closest whole number that is less than or equal to the given value, which may be a fraction.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.floor)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "floor", [value]))

    @jsii.member(jsii_name="format")
    @builtins.classmethod
    def format(
        cls,
        spec: builtins.str,
        values: typing.Sequence[typing.Any],
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/format.html format} produces a string by formatting a number of other values according to a specification string.

        :param spec: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.format)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "format", [spec, values]))

    @jsii.member(jsii_name="formatdate")
    @builtins.classmethod
    def formatdate(cls, spec: builtins.str, timestamp: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/formatdate.html formatdate} converts a timestamp into a different time format.

        :param spec: -
        :param timestamp: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.formatdate)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "formatdate", [spec, timestamp]))

    @jsii.member(jsii_name="formatlist")
    @builtins.classmethod
    def formatlist(
        cls,
        spec: builtins.str,
        values: typing.Sequence[typing.Any],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/formatlist.html formatlist} produces a list of strings by formatting a number of other values according to a specification string.

        :param spec: -
        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.formatlist)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "formatlist", [spec, values]))

    @jsii.member(jsii_name="indent")
    @builtins.classmethod
    def indent(cls, indentation: jsii.Number, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/indent.html indent} adds a given number of spaces to the beginnings of all but the first line in a given multi-line string.

        :param indentation: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.indent)
            check_type(argname="argument indentation", value=indentation, expected_type=type_hints["indentation"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "indent", [indentation, value]))

    @jsii.member(jsii_name="index")
    @builtins.classmethod
    def index(
        cls,
        list: typing.Union[typing.Sequence[typing.Any], "IResolvable"],
        value: typing.Any,
    ) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/index.html index} finds the element index for a given value in a list.

        :param list: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.index)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "index", [list, value]))

    @jsii.member(jsii_name="join")
    @builtins.classmethod
    def join(
        cls,
        separator: builtins.str,
        value: typing.Sequence[builtins.str],
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/join.html join} produces a string by concatenating together all elements of a given list of strings with the given delimiter.

        :param separator: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.join)
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "join", [separator, value]))

    @jsii.member(jsii_name="jsondecode")
    @builtins.classmethod
    def jsondecode(cls, value: builtins.str) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/jsondecode.html jsondecode} interprets a given string as JSON, returning a representation of the result of decoding that string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.jsondecode)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "jsondecode", [value]))

    @jsii.member(jsii_name="jsonencode")
    @builtins.classmethod
    def jsonencode(cls, value: typing.Any) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/jsonencode.html jsonencode} encodes a given value to a string using JSON syntax.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.jsonencode)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "jsonencode", [value]))

    @jsii.member(jsii_name="keys")
    @builtins.classmethod
    def keys(
        cls,
        map: typing.Union["IResolvable", typing.Mapping[builtins.str, typing.Any]],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/keys.html keys} takes a map and returns a list containing the keys from that map.

        :param map: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.keys)
            check_type(argname="argument map", value=map, expected_type=type_hints["map"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "keys", [map]))

    @jsii.member(jsii_name="lengthOf")
    @builtins.classmethod
    def length_of(cls, value: typing.Any) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/length.html length} determines the length of a given list, map, or string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.length_of)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "lengthOf", [value]))

    @jsii.member(jsii_name="log")
    @builtins.classmethod
    def log(cls, value: jsii.Number, base: jsii.Number) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/log.html log} returns the logarithm of a given number in a given base.

        :param value: -
        :param base: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.log)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "log", [value, base]))

    @jsii.member(jsii_name="lookup")
    @builtins.classmethod
    def lookup(
        cls,
        value: typing.Any,
        key: typing.Any,
        default_value: typing.Any,
    ) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/lookup.html lookup} retrieves the value of a single element from a map, given its key. If the given key does not exist, the given default value is returned instead.

        :param value: -
        :param key: -
        :param default_value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.lookup)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "lookup", [value, key, default_value]))

    @jsii.member(jsii_name="lower")
    @builtins.classmethod
    def lower(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/lower.html lower} converts all cased letters in the given string to lowercase.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.lower)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "lower", [value]))

    @jsii.member(jsii_name="matchkeys")
    @builtins.classmethod
    def matchkeys(
        cls,
        values_list: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
        keys_list: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
        search_set: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/matchkeys.html matchkeys} constructs a new list by taking a subset of elements from one list whose indexes match the corresponding indexes of values in another list.

        :param values_list: -
        :param keys_list: -
        :param search_set: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.matchkeys)
            check_type(argname="argument values_list", value=values_list, expected_type=type_hints["values_list"])
            check_type(argname="argument keys_list", value=keys_list, expected_type=type_hints["keys_list"])
            check_type(argname="argument search_set", value=search_set, expected_type=type_hints["search_set"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "matchkeys", [values_list, keys_list, search_set]))

    @jsii.member(jsii_name="max")
    @builtins.classmethod
    def max(cls, values: typing.Sequence[jsii.Number]) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/max.html max} takes one or more numbers and returns the greatest number from the set.

        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.max)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "max", [values]))

    @jsii.member(jsii_name="md5")
    @builtins.classmethod
    def md5(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/md5.html md5} computes the MD5 hash of a given string and encodes it with hexadecimal digits.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.md5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "md5", [value]))

    @jsii.member(jsii_name="mergeLists")
    @builtins.classmethod
    def merge_lists(
        cls,
        values: typing.Sequence[typing.Any],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/merge.html merge} takes an arbitrary number of maps or objects, and returns a single map or object that contains a merged set of elements from all arguments.

        :param values: - Arguments are passed in an array.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.merge_lists)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "mergeLists", [values]))

    @jsii.member(jsii_name="mergeMaps")
    @builtins.classmethod
    def merge_maps(
        cls,
        values: typing.Sequence[typing.Any],
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/merge.html merge} takes an arbitrary number of maps or objects, and returns a single map or object that contains a merged set of elements from all arguments.

        :param values: - Arguments are passed in an array.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.merge_maps)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.sinvoke(cls, "mergeMaps", [values]))

    @jsii.member(jsii_name="min")
    @builtins.classmethod
    def min(cls, values: typing.Sequence[jsii.Number]) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/min.html min} takes one or more numbers and returns the smallest number from the set.

        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.min)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "min", [values]))

    @jsii.member(jsii_name="nonsensitive")
    @builtins.classmethod
    def nonsensitive(cls, expression: typing.Any) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/nonsensitive.html nonsensitive} takes a sensitive value and returns a copy of that value with the sensitive marking removed, thereby exposing the sensitive value.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.nonsensitive)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "nonsensitive", [expression]))

    @jsii.member(jsii_name="one")
    @builtins.classmethod
    def one(
        cls,
        list: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
    ) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/one.html one} takes a list, set, or tuple value with either zero or one elements.

        :param list: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.one)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "one", [list]))

    @jsii.member(jsii_name="parseInt")
    @builtins.classmethod
    def parse_int(cls, value: builtins.str, base: jsii.Number) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/parseint.html parseInt} parses the given string as a representation of an integer in the specified base and returns the resulting number. The base must be between 2 and 62 inclusive.

        :param value: -
        :param base: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.parse_int)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "parseInt", [value, base]))

    @jsii.member(jsii_name="pathexpand")
    @builtins.classmethod
    def pathexpand(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/pathexpand.html pathexpand} takes a string containing a filesystem path and removes the last portion from it.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.pathexpand)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "pathexpand", [value]))

    @jsii.member(jsii_name="pow")
    @builtins.classmethod
    def pow(cls, value: jsii.Number, power: jsii.Number) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/pow.html pow} calculates an exponent, by raising its first argument to the power of the second argument.

        :param value: -
        :param power: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.pow)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument power", value=power, expected_type=type_hints["power"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "pow", [value, power]))

    @jsii.member(jsii_name="range")
    @builtins.classmethod
    def range(
        cls,
        start: jsii.Number,
        limit: jsii.Number,
        step: typing.Optional[jsii.Number] = None,
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/range.html range} generates a list of numbers using a start value, a limit value, and a step value.

        :param start: -
        :param limit: -
        :param step: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.range)
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "range", [start, limit, step]))

    @jsii.member(jsii_name="rawString")
    @builtins.classmethod
    def raw_string(cls, str: builtins.str) -> builtins.str:
        '''(experimental) Use this function to wrap a string and escape it properly for the use in Terraform This is only needed in certain scenarios (e.g., if you have unescaped double quotes in the string).

        :param str: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.raw_string)
            check_type(argname="argument str", value=str, expected_type=type_hints["str"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "rawString", [str]))

    @jsii.member(jsii_name="regex")
    @builtins.classmethod
    def regex(cls, pattern: builtins.str, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/regex.html regex} applies a regular expression to a string and returns the matching substrings in pattern.

        :param pattern: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.regex)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "regex", [pattern, value]))

    @jsii.member(jsii_name="regexall")
    @builtins.classmethod
    def regexall(
        cls,
        pattern: builtins.str,
        value: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/regexall.html regexall} applies a regular expression to a string and returns a list of all matches.

        :param pattern: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.regexall)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "regexall", [pattern, value]))

    @jsii.member(jsii_name="replace")
    @builtins.classmethod
    def replace(
        cls,
        value: builtins.str,
        substring: builtins.str,
        replacement: builtins.str,
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/replace.html replace} searches a given string for another given substring, and replaces each occurrence with a given replacement string.

        :param value: -
        :param substring: -
        :param replacement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.replace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument substring", value=substring, expected_type=type_hints["substring"])
            check_type(argname="argument replacement", value=replacement, expected_type=type_hints["replacement"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "replace", [value, substring, replacement]))

    @jsii.member(jsii_name="reverse")
    @builtins.classmethod
    def reverse(
        cls,
        values: typing.Union[typing.Sequence[typing.Any], "IResolvable"],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/reverse.html reverse} takes a sequence and produces a new sequence of the same length with all of the same elements as the given sequence but in reverse order.

        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.reverse)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "reverse", [values]))

    @jsii.member(jsii_name="rsadecrypt")
    @builtins.classmethod
    def rsadecrypt(
        cls,
        ciphertext: builtins.str,
        privatekey: builtins.str,
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/rsadecrypt.html rsadecrypt} decrypts an RSA-encrypted ciphertext, returning the corresponding cleartext.

        :param ciphertext: -
        :param privatekey: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.rsadecrypt)
            check_type(argname="argument ciphertext", value=ciphertext, expected_type=type_hints["ciphertext"])
            check_type(argname="argument privatekey", value=privatekey, expected_type=type_hints["privatekey"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "rsadecrypt", [ciphertext, privatekey]))

    @jsii.member(jsii_name="sensitive")
    @builtins.classmethod
    def sensitive(cls, expression: typing.Any) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/sensitive.html sensitive} takes any value and returns a copy of it marked so that Terraform will treat it as sensitive, with the same meaning and behavior as for sensitive input variables.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.sensitive)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "sensitive", [expression]))

    @jsii.member(jsii_name="setintersection")
    @builtins.classmethod
    def setintersection(
        cls,
        values: typing.Sequence[typing.Any],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/setintersection.html setintersection} function takes multiple sets and produces a single set containing only the elements that all of the given sets have in common.

        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.setintersection)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "setintersection", [values]))

    @jsii.member(jsii_name="setproduct")
    @builtins.classmethod
    def setproduct(
        cls,
        values: typing.Sequence[typing.Any],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/setproduct.html setproduct} function finds all of the possible combinations of elements from all of the given sets by computing the Cartesian product.

        :param values: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.setproduct)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "setproduct", [values]))

    @jsii.member(jsii_name="setsubtract")
    @builtins.classmethod
    def setsubtract(
        cls,
        minuend: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
        subtrahend: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/slice.html setsubtract} function returns a new set containing the elements from the first set that are not present in the second set.

        :param minuend: -
        :param subtrahend: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.setsubtract)
            check_type(argname="argument minuend", value=minuend, expected_type=type_hints["minuend"])
            check_type(argname="argument subtrahend", value=subtrahend, expected_type=type_hints["subtrahend"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "setsubtract", [minuend, subtrahend]))

    @jsii.member(jsii_name="setunion")
    @builtins.classmethod
    def setunion(cls, values: typing.Sequence[typing.Any]) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/setunion.html setunion} function takes multiple sets and produces a single set containing the elements from all of the given sets.

        :param values: - Arguments are passed in an array.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.setunion)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "setunion", [values]))

    @jsii.member(jsii_name="sha1")
    @builtins.classmethod
    def sha1(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/sha1.html sha1} computes the SHA1 hash of a given string and encodes it with hexadecimal digits.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.sha1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "sha1", [value]))

    @jsii.member(jsii_name="sha256")
    @builtins.classmethod
    def sha256(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/sha256.html sha256} computes the SHA256 hash of a given string and encodes it with hexadecimal digits.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.sha256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "sha256", [value]))

    @jsii.member(jsii_name="sha512")
    @builtins.classmethod
    def sha512(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/sha512.html sha512} computes the SHA512 hash of a given string and encodes it with hexadecimal digits.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.sha512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "sha512", [value]))

    @jsii.member(jsii_name="signum")
    @builtins.classmethod
    def signum(cls, value: jsii.Number) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/signum.html signum} determines the sign of a number, returning a number between -1 and 1 to represent the sign.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.signum)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "signum", [value]))

    @jsii.member(jsii_name="slice")
    @builtins.classmethod
    def slice(
        cls,
        list: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
        startindex: jsii.Number,
        endindex: jsii.Number,
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/slice.html slice} extracts some consecutive elements from within a list.

        :param list: -
        :param startindex: -
        :param endindex: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.slice)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
            check_type(argname="argument startindex", value=startindex, expected_type=type_hints["startindex"])
            check_type(argname="argument endindex", value=endindex, expected_type=type_hints["endindex"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "slice", [list, startindex, endindex]))

    @jsii.member(jsii_name="sort")
    @builtins.classmethod
    def sort(
        cls,
        list: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/sort.html sort} takes a list of strings and returns a new list with those strings sorted lexicographically.

        :param list: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.sort)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "sort", [list]))

    @jsii.member(jsii_name="split")
    @builtins.classmethod
    def split(
        cls,
        seperator: builtins.str,
        value: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/split.html split} produces a list by dividing a given string at all occurrences of a given separator.

        :param seperator: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.split)
            check_type(argname="argument seperator", value=seperator, expected_type=type_hints["seperator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "split", [seperator, value]))

    @jsii.member(jsii_name="strrev")
    @builtins.classmethod
    def strrev(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/strrev.html strrev} reverses the characters in a string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.strrev)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "strrev", [value]))

    @jsii.member(jsii_name="substr")
    @builtins.classmethod
    def substr(
        cls,
        value: builtins.str,
        offset: jsii.Number,
        length: jsii.Number,
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/substr.html substr} extracts a substring from a given string by offset and length.

        :param value: -
        :param offset: -
        :param length: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.substr)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument length", value=length, expected_type=type_hints["length"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "substr", [value, offset, length]))

    @jsii.member(jsii_name="sum")
    @builtins.classmethod
    def sum(
        cls,
        list: typing.Union[builtins.str, typing.Sequence[typing.Any], "IResolvable"],
    ) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/sum.html sum} takes a list or set of numbers and returns the sum of those numbers.

        :param list: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.sum)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "sum", [list]))

    @jsii.member(jsii_name="templatefile")
    @builtins.classmethod
    def templatefile(cls, path: builtins.str, vars: typing.Any) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/templatefile.html templatefile} reads the file at the given path and renders its content as a template using a supplied set of template variables.

        :param path: -
        :param vars: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.templatefile)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument vars", value=vars, expected_type=type_hints["vars"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "templatefile", [path, vars]))

    @jsii.member(jsii_name="textdecodebase64")
    @builtins.classmethod
    def textdecodebase64(
        cls,
        value: builtins.str,
        encoding_name: builtins.str,
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/textdecodebase64.html textdecodebase64} function decodes a string that was previously Base64-encoded, and then interprets the result as characters in a specified character encoding.

        :param value: -
        :param encoding_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.textdecodebase64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument encoding_name", value=encoding_name, expected_type=type_hints["encoding_name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "textdecodebase64", [value, encoding_name]))

    @jsii.member(jsii_name="textencodebase64")
    @builtins.classmethod
    def textencodebase64(
        cls,
        value: builtins.str,
        encoding_name: builtins.str,
    ) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/textencodebase64.html textencodebase64}  encodes the unicode characters in a given string using a specified character encoding, returning the result base64 encoded because Terraform language strings are always sequences of unicode characters.

        :param value: -
        :param encoding_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.textencodebase64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument encoding_name", value=encoding_name, expected_type=type_hints["encoding_name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "textencodebase64", [value, encoding_name]))

    @jsii.member(jsii_name="timeadd")
    @builtins.classmethod
    def timeadd(cls, timestamp: builtins.str, duration: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/timeadd.html timeadd} adds a duration to a timestamp, returning a new timestamp.

        :param timestamp: -
        :param duration: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.timeadd)
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "timeadd", [timestamp, duration]))

    @jsii.member(jsii_name="timestamp")
    @builtins.classmethod
    def timestamp(cls) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/timestamp.html timestamp} returns a UTC timestamp string in RFC 3339 format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "timestamp", []))

    @jsii.member(jsii_name="title")
    @builtins.classmethod
    def title(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/title.html title} converts the first letter of each word in the given string to uppercase.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.title)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "title", [value]))

    @jsii.member(jsii_name="tobool")
    @builtins.classmethod
    def tobool(cls, expression: typing.Any) -> "IResolvable":
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/tobool.html tobool} converts its argument to a boolean value.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.tobool)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast("IResolvable", jsii.sinvoke(cls, "tobool", [expression]))

    @jsii.member(jsii_name="tolist")
    @builtins.classmethod
    def tolist(cls, expression: typing.Any) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/tolist.html tolist} converts its argument to a list value.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.tolist)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "tolist", [expression]))

    @jsii.member(jsii_name="tomap")
    @builtins.classmethod
    def tomap(cls, expression: typing.Any) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/tomap.html tomap} converts its argument to a map value.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.tomap)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "tomap", [expression]))

    @jsii.member(jsii_name="tonumber")
    @builtins.classmethod
    def tonumber(cls, expression: typing.Any) -> jsii.Number:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/tonumber.html tonumber} converts its argument to a number value.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.tonumber)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "tonumber", [expression]))

    @jsii.member(jsii_name="toset")
    @builtins.classmethod
    def toset(cls, expression: typing.Any) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/toset.html toset} converts its argument to a set value.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.toset)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "toset", [expression]))

    @jsii.member(jsii_name="tostring")
    @builtins.classmethod
    def tostring(cls, expression: typing.Any) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/tostring.html tostring} converts its argument to a string value.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.tostring)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "tostring", [expression]))

    @jsii.member(jsii_name="transpose")
    @builtins.classmethod
    def transpose(cls, value: typing.Any) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/transpose.html transpose} takes a map of lists of strings and swaps the keys and values to produce a new map of lists of strings.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.transpose)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "transpose", [value]))

    @jsii.member(jsii_name="trim")
    @builtins.classmethod
    def trim(cls, value: builtins.str, replacement: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/trim.html trim} removes the specified characters from the start and end of the given string.

        :param value: -
        :param replacement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.trim)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument replacement", value=replacement, expected_type=type_hints["replacement"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "trim", [value, replacement]))

    @jsii.member(jsii_name="trimprefix")
    @builtins.classmethod
    def trimprefix(cls, value: builtins.str, prefix: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/trimprefix.html trimprefix} removes the specified prefix from the start of the given string.

        :param value: -
        :param prefix: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.trimprefix)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "trimprefix", [value, prefix]))

    @jsii.member(jsii_name="trimspace")
    @builtins.classmethod
    def trimspace(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/trimspace.html trimspace} removes any space characters from the start and end of the given string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.trimspace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "trimspace", [value]))

    @jsii.member(jsii_name="trimsuffix")
    @builtins.classmethod
    def trimsuffix(cls, value: builtins.str, suffix: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/trimsuffix.html trimsuffix} removes the specified suffix from the end of the given string.

        :param value: -
        :param suffix: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.trimsuffix)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "trimsuffix", [value, suffix]))

    @jsii.member(jsii_name="try")
    @builtins.classmethod
    def try_(cls, expression: typing.Sequence[typing.Any]) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/try.html try} evaluates all of its argument expressions in turn and returns the result of the first one that does not produce any errors.

        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.try_)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "try", [expression]))

    @jsii.member(jsii_name="upper")
    @builtins.classmethod
    def upper(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/upper.html upper} converts all cased letters in the given string to uppercase.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.upper)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "upper", [value]))

    @jsii.member(jsii_name="urlencode")
    @builtins.classmethod
    def urlencode(cls, value: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/urlencode.html urlencode} applies URL encoding to a given string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.urlencode)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "urlencode", [value]))

    @jsii.member(jsii_name="uuid")
    @builtins.classmethod
    def uuid(cls) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/uuid.html uuid} generates a unique identifier string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "uuid", []))

    @jsii.member(jsii_name="uuidv5")
    @builtins.classmethod
    def uuidv5(cls, namespace: builtins.str, name: builtins.str) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/uuidv5.html uuidv5} generates a unique identifier string.

        :param namespace: -
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.uuidv5)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "uuidv5", [namespace, name]))

    @jsii.member(jsii_name="values")
    @builtins.classmethod
    def values(cls, value: typing.Any) -> typing.List[builtins.str]:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/values.html values} takes a map and returns a list containing the values of the elements in that map.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.values)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "values", [value]))

    @jsii.member(jsii_name="yamldecode")
    @builtins.classmethod
    def yamldecode(cls, value: builtins.str) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/yamldecode.html yamldecode} parses a string as a subset of YAML, and produces a representation of its value.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.yamldecode)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "yamldecode", [value]))

    @jsii.member(jsii_name="yamlencode")
    @builtins.classmethod
    def yamlencode(cls, value: typing.Any) -> builtins.str:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/yamlencode.html yamlencode} encodes a given value to a string using JSON syntax.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.yamlencode)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "yamlencode", [value]))

    @jsii.member(jsii_name="zipmap")
    @builtins.classmethod
    def zipmap(
        cls,
        keyslist: typing.Union[typing.Sequence[typing.Any], "IResolvable"],
        valueslist: typing.Union[typing.Sequence[typing.Any], "IResolvable"],
    ) -> typing.Any:
        '''(experimental) {@link https://www.terraform.io/docs/language/functions/zipmap.html zipmap} constructs a map from a list of keys and a corresponding list of values.

        :param keyslist: -
        :param valueslist: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Fn.zipmap)
            check_type(argname="argument keyslist", value=keyslist, expected_type=type_hints["keyslist"])
            check_type(argname="argument valueslist", value=valueslist, expected_type=type_hints["valueslist"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "zipmap", [keyslist, valueslist]))


@jsii.data_type(
    jsii_type="cdktf.GcsBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "access_token": "accessToken",
        "credentials": "credentials",
        "encryption_key": "encryptionKey",
        "impersonate_service_account": "impersonateServiceAccount",
        "impersonate_service_account_delegates": "impersonateServiceAccountDelegates",
        "prefix": "prefix",
    },
)
class GcsBackendProps:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        impersonate_service_account: typing.Optional[builtins.str] = None,
        impersonate_service_account_delegates: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Stores the state as an object in a configurable prefix in a pre-existing bucket on Google Cloud Storage (GCS).

        The bucket must exist prior to configuring the backend.

        This backend supports state locking.

        Warning! It is highly recommended that you enable Object Versioning on the GCS bucket
        to allow for state recovery in the case of accidental deletions and human error.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/gcs

        :param bucket: (experimental) (Required) The name of the GCS bucket. This name must be globally unique.
        :param access_token: (experimental) (Optional) A temporary [OAuth 2.0 access token] obtained from the Google Authorization server, i.e. the Authorization: Bearer token used to authenticate HTTP requests to GCP APIs. This is an alternative to credentials. If both are specified, access_token will be used over the credentials field.
        :param credentials: (experimental) (Optional) Local path to Google Cloud Platform account credentials in JSON format. If unset, Google Application Default Credentials are used. The provided credentials must have Storage Object Admin role on the bucket. Warning: if using the Google Cloud Platform provider as well, it will also pick up the GOOGLE_CREDENTIALS environment variable.
        :param encryption_key: (experimental) (Optional) A 32 byte base64 encoded 'customer supplied encryption key' used to encrypt all state.
        :param impersonate_service_account: (experimental) (Optional) The service account to impersonate for accessing the State Bucket. You must have roles/iam.serviceAccountTokenCreator role on that account for the impersonation to succeed. If you are using a delegation chain, you can specify that using the impersonate_service_account_delegates field. Alternatively, this can be specified using the GOOGLE_IMPERSONATE_SERVICE_ACCOUNT environment variable.
        :param impersonate_service_account_delegates: (experimental) (Optional) The delegation chain for an impersonating a service account.
        :param prefix: (experimental) (Optional) GCS prefix inside the bucket. Named states for workspaces are stored in an object called /.tfstate.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GcsBackendProps.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument impersonate_service_account", value=impersonate_service_account, expected_type=type_hints["impersonate_service_account"])
            check_type(argname="argument impersonate_service_account_delegates", value=impersonate_service_account_delegates, expected_type=type_hints["impersonate_service_account_delegates"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if credentials is not None:
            self._values["credentials"] = credentials
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if impersonate_service_account is not None:
            self._values["impersonate_service_account"] = impersonate_service_account
        if impersonate_service_account_delegates is not None:
            self._values["impersonate_service_account_delegates"] = impersonate_service_account_delegates
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> builtins.str:
        '''(experimental) (Required) The name of the GCS bucket.

        This name must be globally unique.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A temporary [OAuth 2.0 access token] obtained from the Google Authorization server, i.e. the Authorization: Bearer token used to authenticate HTTP requests to GCP APIs. This is an alternative to credentials. If both are specified, access_token will be used over the credentials field.

        :stability: experimental
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Local path to Google Cloud Platform account credentials in JSON format.

        If unset, Google Application Default Credentials are used.
        The provided credentials must have Storage Object Admin role on the bucket.

        Warning: if using the Google Cloud Platform provider as well,
        it will also pick up the GOOGLE_CREDENTIALS environment variable.

        :stability: experimental
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A 32 byte base64 encoded 'customer supplied encryption key' used to encrypt all state.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def impersonate_service_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The service account to impersonate for accessing the State Bucket.

        You must have roles/iam.serviceAccountTokenCreator role on that account for the impersonation to succeed.
        If you are using a delegation chain, you can specify that using the impersonate_service_account_delegates field.
        Alternatively, this can be specified using the GOOGLE_IMPERSONATE_SERVICE_ACCOUNT environment variable.

        :stability: experimental
        '''
        result = self._values.get("impersonate_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def impersonate_service_account_delegates(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) (Optional) The delegation chain for an impersonating a service account.

        :stability: experimental
        '''
        result = self._values.get("impersonate_service_account_delegates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) GCS prefix inside the bucket.

        Named states for workspaces are stored in an object called /.tfstate.

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GcsBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.HttpBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "lock_address": "lockAddress",
        "lock_method": "lockMethod",
        "password": "password",
        "retry_max": "retryMax",
        "retry_wait_max": "retryWaitMax",
        "retry_wait_min": "retryWaitMin",
        "skip_cert_verification": "skipCertVerification",
        "unlock_address": "unlockAddress",
        "unlock_method": "unlockMethod",
        "update_method": "updateMethod",
        "username": "username",
    },
)
class HttpBackendProps:
    def __init__(
        self,
        *,
        address: builtins.str,
        lock_address: typing.Optional[builtins.str] = None,
        lock_method: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        retry_max: typing.Optional[jsii.Number] = None,
        retry_wait_max: typing.Optional[jsii.Number] = None,
        retry_wait_min: typing.Optional[jsii.Number] = None,
        skip_cert_verification: typing.Optional[builtins.bool] = None,
        unlock_address: typing.Optional[builtins.str] = None,
        unlock_method: typing.Optional[builtins.str] = None,
        update_method: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Stores the state using a simple REST client.

        State will be fetched via GET, updated via POST, and purged with DELETE.
        The method used for updating is configurable.

        This backend optionally supports state locking.
        When locking support is enabled it will use LOCK and UNLOCK requests providing the lock info in the body.
        The endpoint should return a 423: Locked or 409: Conflict with the holding lock info when
        it's already taken, 200: OK for success. Any other status will be considered an error.
        The ID of the holding lock info will be added as a query parameter to state updates requests.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/http

        :param address: (experimental) (Required) The address of the REST endpoint.
        :param lock_address: (experimental) (Optional) The address of the lock REST endpoint. Defaults to disabled.
        :param lock_method: (experimental) (Optional) The HTTP method to use when locking. Defaults to LOCK.
        :param password: (experimental) (Optional) The password for HTTP basic authentication.
        :param retry_max: (experimental) (Optional) The number of HTTP request retries. Defaults to 2.
        :param retry_wait_max: (experimental) (Optional) The maximum time in seconds to wait between HTTP request attempts. Defaults to 30.
        :param retry_wait_min: (experimental) (Optional) The minimum time in seconds to wait between HTTP request attempts. Defaults to 1.
        :param skip_cert_verification: (experimental) (Optional) Whether to skip TLS verification. Defaults to false.
        :param unlock_address: (experimental) (Optional) The address of the unlock REST endpoint. Defaults to disabled.
        :param unlock_method: (experimental) (Optional) The HTTP method to use when unlocking. Defaults to UNLOCK.
        :param update_method: (experimental) (Optional) HTTP method to use when updating state. Defaults to POST.
        :param username: (experimental) (Optional) The username for HTTP basic authentication.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpBackendProps.__init__)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument lock_address", value=lock_address, expected_type=type_hints["lock_address"])
            check_type(argname="argument lock_method", value=lock_method, expected_type=type_hints["lock_method"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument retry_max", value=retry_max, expected_type=type_hints["retry_max"])
            check_type(argname="argument retry_wait_max", value=retry_wait_max, expected_type=type_hints["retry_wait_max"])
            check_type(argname="argument retry_wait_min", value=retry_wait_min, expected_type=type_hints["retry_wait_min"])
            check_type(argname="argument skip_cert_verification", value=skip_cert_verification, expected_type=type_hints["skip_cert_verification"])
            check_type(argname="argument unlock_address", value=unlock_address, expected_type=type_hints["unlock_address"])
            check_type(argname="argument unlock_method", value=unlock_method, expected_type=type_hints["unlock_method"])
            check_type(argname="argument update_method", value=update_method, expected_type=type_hints["update_method"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "address": address,
        }
        if lock_address is not None:
            self._values["lock_address"] = lock_address
        if lock_method is not None:
            self._values["lock_method"] = lock_method
        if password is not None:
            self._values["password"] = password
        if retry_max is not None:
            self._values["retry_max"] = retry_max
        if retry_wait_max is not None:
            self._values["retry_wait_max"] = retry_wait_max
        if retry_wait_min is not None:
            self._values["retry_wait_min"] = retry_wait_min
        if skip_cert_verification is not None:
            self._values["skip_cert_verification"] = skip_cert_verification
        if unlock_address is not None:
            self._values["unlock_address"] = unlock_address
        if unlock_method is not None:
            self._values["unlock_method"] = unlock_method
        if update_method is not None:
            self._values["update_method"] = update_method
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def address(self) -> builtins.str:
        '''(experimental) (Required) The address of the REST endpoint.

        :stability: experimental
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lock_address(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The address of the lock REST endpoint.

        Defaults to disabled.

        :stability: experimental
        '''
        result = self._values.get("lock_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_method(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The HTTP method to use when locking.

        Defaults to LOCK.

        :stability: experimental
        '''
        result = self._values.get("lock_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The password for HTTP basic authentication.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_max(self) -> typing.Optional[jsii.Number]:
        '''(experimental) (Optional) The number of HTTP request retries.

        Defaults to 2.

        :stability: experimental
        '''
        result = self._values.get("retry_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_wait_max(self) -> typing.Optional[jsii.Number]:
        '''(experimental) (Optional) The maximum time in seconds to wait between HTTP request attempts.

        Defaults to 30.

        :stability: experimental
        '''
        result = self._values.get("retry_wait_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_wait_min(self) -> typing.Optional[jsii.Number]:
        '''(experimental) (Optional) The minimum time in seconds to wait between HTTP request attempts.

        Defaults to 1.

        :stability: experimental
        '''
        result = self._values.get("retry_wait_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def skip_cert_verification(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Whether to skip TLS verification.

        Defaults to false.

        :stability: experimental
        '''
        result = self._values.get("skip_cert_verification")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def unlock_address(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The address of the unlock REST endpoint.

        Defaults to disabled.

        :stability: experimental
        '''
        result = self._values.get("unlock_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unlock_method(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The HTTP method to use when unlocking.

        Defaults to UNLOCK.

        :stability: experimental
        '''
        result = self._values.get("unlock_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_method(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) HTTP method to use when updating state.

        Defaults to POST.

        :stability: experimental
        '''
        result = self._values.get("update_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The username for HTTP basic authentication.

        :stability: experimental
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdktf.IAnyProducer")
class IAnyProducer(typing_extensions.Protocol):
    '''(experimental) Interface for lazy untyped value producers.

    :stability: experimental
    '''

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        '''(experimental) Produce the value.

        :param context: -

        :stability: experimental
        '''
        ...


class _IAnyProducerProxy:
    '''(experimental) Interface for lazy untyped value producers.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IAnyProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        '''(experimental) Produce the value.

        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IAnyProducer.produce)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "produce", [context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAnyProducer).__jsii_proxy_class__ = lambda : _IAnyProducerProxy


@jsii.interface(jsii_type="cdktf.IAspect")
class IAspect(typing_extensions.Protocol):
    '''(experimental) Represents an Aspect.

    :stability: experimental
    '''

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''(experimental) All aspects can visit an IConstruct.

        :param node: -

        :stability: experimental
        '''
        ...


class _IAspectProxy:
    '''(experimental) Represents an Aspect.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IAspect"

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''(experimental) All aspects can visit an IConstruct.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IAspect.visit)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAspect).__jsii_proxy_class__ = lambda : _IAspectProxy


@jsii.interface(jsii_type="cdktf.IFragmentConcatenator")
class IFragmentConcatenator(typing_extensions.Protocol):
    '''(experimental) Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    :stability: experimental
    '''

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        '''(experimental) Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        ...


class _IFragmentConcatenatorProxy:
    '''(experimental) Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IFragmentConcatenator"

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        '''(experimental) Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IFragmentConcatenator.join)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast(typing.Any, jsii.invoke(self, "join", [left, right]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFragmentConcatenator).__jsii_proxy_class__ = lambda : _IFragmentConcatenatorProxy


@jsii.interface(jsii_type="cdktf.IInterpolatingParent")
class IInterpolatingParent(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> "IResolvable":
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        ...


class _IInterpolatingParentProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IInterpolatingParent"

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> "IResolvable":
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IInterpolatingParent.interpolation_for_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast("IResolvable", jsii.invoke(self, "interpolationForAttribute", [terraform_attribute]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInterpolatingParent).__jsii_proxy_class__ = lambda : _IInterpolatingParentProxy


@jsii.interface(jsii_type="cdktf.IListProducer")
class IListProducer(typing_extensions.Protocol):
    '''(experimental) Interface for lazy list producers.

    :stability: experimental
    '''

    @jsii.member(jsii_name="produce")
    def produce(
        self,
        context: "IResolveContext",
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Produce the list value.

        :param context: -

        :stability: experimental
        '''
        ...


class _IListProducerProxy:
    '''(experimental) Interface for lazy list producers.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IListProducer"

    @jsii.member(jsii_name="produce")
    def produce(
        self,
        context: "IResolveContext",
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Produce the list value.

        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IListProducer.produce)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.invoke(self, "produce", [context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IListProducer).__jsii_proxy_class__ = lambda : _IListProducerProxy


@jsii.interface(jsii_type="cdktf.IManifest")
class IManifest(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.Mapping[builtins.str, "StackManifest"]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _IManifestProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IManifest"

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.Mapping[builtins.str, "StackManifest"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "StackManifest"], jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManifest).__jsii_proxy_class__ = lambda : _IManifestProxy


@jsii.interface(jsii_type="cdktf.INumberProducer")
class INumberProducer(typing_extensions.Protocol):
    '''(experimental) Interface for lazy number producers.

    :stability: experimental
    '''

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        '''(experimental) Produce the number value.

        :param context: -

        :stability: experimental
        '''
        ...


class _INumberProducerProxy:
    '''(experimental) Interface for lazy number producers.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.INumberProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        '''(experimental) Produce the number value.

        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(INumberProducer.produce)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Optional[jsii.Number], jsii.invoke(self, "produce", [context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INumberProducer).__jsii_proxy_class__ = lambda : _INumberProducerProxy


@jsii.interface(jsii_type="cdktf.IPostProcessor")
class IPostProcessor(typing_extensions.Protocol):
    '''(experimental) A Token that can post-process the complete resolved value, after resolve() has recursed over it.

    :stability: experimental
    '''

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        '''(experimental) Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -

        :stability: experimental
        '''
        ...


class _IPostProcessorProxy:
    '''(experimental) A Token that can post-process the complete resolved value, after resolve() has recursed over it.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IPostProcessor"

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        '''(experimental) Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IPostProcessor.post_process)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "postProcess", [input, context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPostProcessor).__jsii_proxy_class__ = lambda : _IPostProcessorProxy


@jsii.interface(jsii_type="cdktf.IRemoteWorkspace")
class IRemoteWorkspace(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    pass


class _IRemoteWorkspaceProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IRemoteWorkspace"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRemoteWorkspace).__jsii_proxy_class__ = lambda : _IRemoteWorkspaceProxy


@jsii.interface(jsii_type="cdktf.IResolvable")
class IResolvable(typing_extensions.Protocol):
    '''(experimental) Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param context: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        ...


class _IResolvableProxy:
    '''(experimental) Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IResolvable"

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IResolvable.resolve)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResolvable).__jsii_proxy_class__ = lambda : _IResolvableProxy


@jsii.interface(jsii_type="cdktf.IResolveContext")
class IResolveContext(typing_extensions.Protocol):
    '''(experimental) Current resolution context for tokens.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> builtins.bool:
        '''(experimental) True when we are still preparing, false if we're rendering the final output.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.IConstruct:
        '''(experimental) The scope from which resolution has been initiated.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="iteratorContext")
    def iterator_context(self) -> typing.Optional[builtins.str]:
        '''(experimental) TerraformIterators can be passed for block attributes and normal list attributes both require different handling when the iterable variable is accessed e.g. a dynamic block needs each.key while a for expression just needs key.

        :stability: experimental
        '''
        ...

    @iterator_context.setter
    def iterator_context(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="suppressBraces")
    def suppress_braces(self) -> typing.Optional[builtins.bool]:
        '''(experimental) True when ${} should be ommitted (because already inside them), false otherwise.

        :stability: experimental
        '''
        ...

    @suppress_braces.setter
    def suppress_braces(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: IPostProcessor) -> None:
        '''(experimental) Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        '''(experimental) Resolve an inner object.

        :param x: -

        :stability: experimental
        '''
        ...


class _IResolveContextProxy:
    '''(experimental) Current resolution context for tokens.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IResolveContext"

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> builtins.bool:
        '''(experimental) True when we are still preparing, false if we're rendering the final output.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "preparing"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.IConstruct:
        '''(experimental) The scope from which resolution has been initiated.

        :stability: experimental
        '''
        return typing.cast(constructs.IConstruct, jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="iteratorContext")
    def iterator_context(self) -> typing.Optional[builtins.str]:
        '''(experimental) TerraformIterators can be passed for block attributes and normal list attributes both require different handling when the iterable variable is accessed e.g. a dynamic block needs each.key while a for expression just needs key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iteratorContext"))

    @iterator_context.setter
    def iterator_context(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(IResolveContext, "iterator_context").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iteratorContext", value)

    @builtins.property
    @jsii.member(jsii_name="suppressBraces")
    def suppress_braces(self) -> typing.Optional[builtins.bool]:
        '''(experimental) True when ${} should be ommitted (because already inside them), false otherwise.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "suppressBraces"))

    @suppress_braces.setter
    def suppress_braces(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(IResolveContext, "suppress_braces").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppressBraces", value)

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: IPostProcessor) -> None:
        '''(experimental) Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IResolveContext.register_post_processor)
            check_type(argname="argument post_processor", value=post_processor, expected_type=type_hints["post_processor"])
        return typing.cast(None, jsii.invoke(self, "registerPostProcessor", [post_processor]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        '''(experimental) Resolve an inner object.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IResolveContext.resolve)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [x]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResolveContext).__jsii_proxy_class__ = lambda : _IResolveContextProxy


@jsii.interface(jsii_type="cdktf.IResource")
class IResource(constructs.IConstruct, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        '''(experimental) The stack in which this resource is defined.

        :stability: experimental
        '''
        ...


class _IResourceProxy(
    jsii.proxy_for(constructs.IConstruct), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IResource"

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        '''(experimental) The stack in which this resource is defined.

        :stability: experimental
        '''
        return typing.cast("TerraformStack", jsii.get(self, "stack"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResource).__jsii_proxy_class__ = lambda : _IResourceProxy


@jsii.interface(jsii_type="cdktf.IResourceConstructor")
class IResourceConstructor(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    pass


class _IResourceConstructorProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IResourceConstructor"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResourceConstructor).__jsii_proxy_class__ = lambda : _IResourceConstructorProxy


@jsii.interface(jsii_type="cdktf.IScopeCallback")
class IScopeCallback(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    pass


class _IScopeCallbackProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IScopeCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IScopeCallback).__jsii_proxy_class__ = lambda : _IScopeCallbackProxy


@jsii.interface(jsii_type="cdktf.IStackSynthesizer")
class IStackSynthesizer(typing_extensions.Protocol):
    '''(experimental) Encodes information how a certain Stack should be deployed inspired by AWS CDK v2 implementation (synth functionality was removed in constructs v10).

    :stability: experimental
    '''

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: "ISynthesisSession") -> None:
        '''(experimental) Synthesize the associated stack to the session.

        :param session: -

        :stability: experimental
        '''
        ...


class _IStackSynthesizerProxy:
    '''(experimental) Encodes information how a certain Stack should be deployed inspired by AWS CDK v2 implementation (synth functionality was removed in constructs v10).

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IStackSynthesizer"

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: "ISynthesisSession") -> None:
        '''(experimental) Synthesize the associated stack to the session.

        :param session: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IStackSynthesizer.synthesize)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
        return typing.cast(None, jsii.invoke(self, "synthesize", [session]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStackSynthesizer).__jsii_proxy_class__ = lambda : _IStackSynthesizerProxy


@jsii.interface(jsii_type="cdktf.IStringProducer")
class IStringProducer(typing_extensions.Protocol):
    '''(experimental) Interface for lazy string producers.

    :stability: experimental
    '''

    @jsii.member(jsii_name="produce")
    def produce(self, context: IResolveContext) -> typing.Optional[builtins.str]:
        '''(experimental) Produce the string value.

        :param context: -

        :stability: experimental
        '''
        ...


class _IStringProducerProxy:
    '''(experimental) Interface for lazy string producers.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.IStringProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: IResolveContext) -> typing.Optional[builtins.str]:
        '''(experimental) Produce the string value.

        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IStringProducer.produce)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "produce", [context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStringProducer).__jsii_proxy_class__ = lambda : _IStringProducerProxy


@jsii.interface(jsii_type="cdktf.ISynthesisSession")
class ISynthesisSession(typing_extensions.Protocol):
    '''(experimental) Represents a single session of synthesis.

    Passed into ``TerraformStack.onSynthesize()`` methods.
    originally from aws/constructs lib v3.3.126 (synth functionality was removed in constructs v10)

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "Manifest":
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''(experimental) The output directory for this synthesis session.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        ...


class _ISynthesisSessionProxy:
    '''(experimental) Represents a single session of synthesis.

    Passed into ``TerraformStack.onSynthesize()`` methods.
    originally from aws/constructs lib v3.3.126 (synth functionality was removed in constructs v10)

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.ISynthesisSession"

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "Manifest":
        '''
        :stability: experimental
        '''
        return typing.cast("Manifest", jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''(experimental) The output directory for this synthesis session.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipValidation"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISynthesisSession).__jsii_proxy_class__ = lambda : _ISynthesisSessionProxy


@jsii.interface(jsii_type="cdktf.ITerraformAddressable")
class ITerraformAddressable(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _ITerraformAddressableProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.ITerraformAddressable"

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITerraformAddressable).__jsii_proxy_class__ = lambda : _ITerraformAddressableProxy


@jsii.interface(jsii_type="cdktf.ITerraformDependable")
class ITerraformDependable(ITerraformAddressable, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    pass


class _ITerraformDependableProxy(
    jsii.proxy_for(ITerraformAddressable), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.ITerraformDependable"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITerraformDependable).__jsii_proxy_class__ = lambda : _ITerraformDependableProxy


@jsii.interface(jsii_type="cdktf.ITerraformIterator")
class ITerraformIterator(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    pass


class _ITerraformIteratorProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.ITerraformIterator"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITerraformIterator).__jsii_proxy_class__ = lambda : _ITerraformIteratorProxy


@jsii.interface(jsii_type="cdktf.ITerraformResource")
class ITerraformResource(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        ...

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        ...

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="forEach")
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        ...

    @for_each.setter
    def for_each(self, value: typing.Optional[ITerraformIterator]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        '''
        :stability: experimental
        '''
        ...

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        '''
        :stability: experimental
        '''
        ...

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        ...

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> IResolvable:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        ...


class _ITerraformResourceProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.ITerraformResource"

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "friendlyUniqueId"))

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformResourceType"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "count"))

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ITerraformResource, "count").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ITerraformResource, "depends_on").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="forEach")
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[ITerraformIterator], jsii.get(self, "forEach"))

    @for_each.setter
    def for_each(self, value: typing.Optional[ITerraformIterator]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ITerraformResource, "for_each").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forEach", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["TerraformResourceLifecycle"], jsii.get(self, "lifecycle"))

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ITerraformResource, "lifecycle").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["TerraformProvider"], jsii.get(self, "provider"))

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ITerraformResource, "provider").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provider", value)

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> IResolvable:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITerraformResource.interpolation_for_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [terraform_attribute]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITerraformResource).__jsii_proxy_class__ = lambda : _ITerraformResourceProxy


@jsii.interface(jsii_type="cdktf.ITokenMapper")
class ITokenMapper(typing_extensions.Protocol):
    '''(experimental) Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.

    :stability: experimental
    '''

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: IResolvable) -> typing.Any:
        '''(experimental) Replace a single token.

        :param t: -

        :stability: experimental
        '''
        ...


class _ITokenMapperProxy:
    '''(experimental) Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.ITokenMapper"

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: IResolvable) -> typing.Any:
        '''(experimental) Replace a single token.

        :param t: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITokenMapper.map_token)
            check_type(argname="argument t", value=t, expected_type=type_hints["t"])
        return typing.cast(typing.Any, jsii.invoke(self, "mapToken", [t]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITokenMapper).__jsii_proxy_class__ = lambda : _ITokenMapperProxy


@jsii.interface(jsii_type="cdktf.ITokenResolver")
class ITokenResolver(typing_extensions.Protocol):
    '''(experimental) How to resolve tokens.

    :stability: experimental
    '''

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self,
        l: typing.Sequence[builtins.str],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve a tokenized list.

        :param l: -
        :param context: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="resolveMap")
    def resolve_map(
        self,
        m: typing.Mapping[builtins.str, typing.Any],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve a tokenized map.

        :param m: -
        :param context: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="resolveNumberList")
    def resolve_number_list(
        self,
        l: typing.Sequence[jsii.Number],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve a tokenized number list.

        :param l: -
        :param context: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self,
        s: "TokenizedStringFragments",
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: IResolvable,
        context: IResolveContext,
        post_processor: IPostProcessor,
    ) -> typing.Any:
        '''(experimental) Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -

        :stability: experimental
        '''
        ...


class _ITokenResolverProxy:
    '''(experimental) How to resolve tokens.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdktf.ITokenResolver"

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self,
        l: typing.Sequence[builtins.str],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve a tokenized list.

        :param l: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITokenResolver.resolve_list)
            check_type(argname="argument l", value=l, expected_type=type_hints["l"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveList", [l, context]))

    @jsii.member(jsii_name="resolveMap")
    def resolve_map(
        self,
        m: typing.Mapping[builtins.str, typing.Any],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve a tokenized map.

        :param m: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITokenResolver.resolve_map)
            check_type(argname="argument m", value=m, expected_type=type_hints["m"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveMap", [m, context]))

    @jsii.member(jsii_name="resolveNumberList")
    def resolve_number_list(
        self,
        l: typing.Sequence[jsii.Number],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve a tokenized number list.

        :param l: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITokenResolver.resolve_number_list)
            check_type(argname="argument l", value=l, expected_type=type_hints["l"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveNumberList", [l, context]))

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self,
        s: "TokenizedStringFragments",
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITokenResolver.resolve_string)
            check_type(argname="argument s", value=s, expected_type=type_hints["s"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveString", [s, context]))

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: IResolvable,
        context: IResolveContext,
        post_processor: IPostProcessor,
    ) -> typing.Any:
        '''(experimental) Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITokenResolver.resolve_token)
            check_type(argname="argument t", value=t, expected_type=type_hints["t"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument post_processor", value=post_processor, expected_type=type_hints["post_processor"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveToken", [t, context, post_processor]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITokenResolver).__jsii_proxy_class__ = lambda : _ITokenResolverProxy


class Lazy(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Lazy"):
    '''(experimental) Lazily produce a value.

    Can be used to return a string, list or numeric value whose actual value
    will only be calculated later, during synthesis.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="anyValue")
    @builtins.classmethod
    def any_value(
        cls,
        producer: IAnyProducer,
        *,
        display_hint: typing.Optional[builtins.str] = None,
        omit_empty_array: typing.Optional[builtins.bool] = None,
    ) -> IResolvable:
        '''(experimental) Produces a lazy token from an untyped value.

        :param producer: The lazy producer.
        :param display_hint: (experimental) Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: (experimental) If the produced value is an array and it is empty, return 'undefined' instead. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Lazy.any_value)
            check_type(argname="argument producer", value=producer, expected_type=type_hints["producer"])
        options = LazyAnyValueOptions(
            display_hint=display_hint, omit_empty_array=omit_empty_array
        )

        return typing.cast(IResolvable, jsii.sinvoke(cls, "anyValue", [producer, options]))

    @jsii.member(jsii_name="listValue")
    @builtins.classmethod
    def list_value(
        cls,
        producer: IListProducer,
        *,
        display_hint: typing.Optional[builtins.str] = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns a list-ified token for a lazy value.

        :param producer: The producer.
        :param display_hint: (experimental) Use the given name as a display hint. Default: - No hint
        :param omit_empty: (experimental) If the produced list is empty, return 'undefined' instead. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Lazy.list_value)
            check_type(argname="argument producer", value=producer, expected_type=type_hints["producer"])
        options = LazyListValueOptions(
            display_hint=display_hint, omit_empty=omit_empty
        )

        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "listValue", [producer, options]))

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(cls, producer: INumberProducer) -> jsii.Number:
        '''(experimental) Returns a numberified token for a lazy value.

        :param producer: The producer.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Lazy.number_value)
            check_type(argname="argument producer", value=producer, expected_type=type_hints["producer"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "numberValue", [producer]))

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(
        cls,
        producer: IStringProducer,
        *,
        display_hint: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Returns a stringified token for a lazy value.

        :param producer: The producer.
        :param display_hint: (experimental) Use the given name as a display hint. Default: - No hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Lazy.string_value)
            check_type(argname="argument producer", value=producer, expected_type=type_hints["producer"])
        options = LazyStringValueOptions(display_hint=display_hint)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "stringValue", [producer, options]))


@jsii.data_type(
    jsii_type="cdktf.LazyAnyValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint", "omit_empty_array": "omitEmptyArray"},
)
class LazyAnyValueOptions:
    def __init__(
        self,
        *,
        display_hint: typing.Optional[builtins.str] = None,
        omit_empty_array: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for creating lazy untyped tokens.

        :param display_hint: (experimental) Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: (experimental) If the produced value is an array and it is empty, return 'undefined' instead. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LazyAnyValueOptions.__init__)
            check_type(argname="argument display_hint", value=display_hint, expected_type=type_hints["display_hint"])
            check_type(argname="argument omit_empty_array", value=omit_empty_array, expected_type=type_hints["omit_empty_array"])
        self._values: typing.Dict[str, typing.Any] = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint
        if omit_empty_array is not None:
            self._values["omit_empty_array"] = omit_empty_array

    @builtins.property
    def display_hint(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the given name as a display hint.

        :default: - No hint

        :stability: experimental
        '''
        result = self._values.get("display_hint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def omit_empty_array(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the produced value is an array and it is empty, return 'undefined' instead.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty_array")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyAnyValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IResolvable)
class LazyBase(metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.LazyBase"):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addPostProcessor")
    def add_post_processor(self, post_processor: IPostProcessor) -> None:
        '''
        :param post_processor: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LazyBase.add_post_processor)
            check_type(argname="argument post_processor", value=post_processor, expected_type=type_hints["post_processor"])
        return typing.cast(None, jsii.invoke(self, "addPostProcessor", [post_processor]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LazyBase.resolve)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [context]))

    @jsii.member(jsii_name="resolveLazy")
    @abc.abstractmethod
    def _resolve_lazy(self, context: IResolveContext) -> typing.Any:
        '''
        :param context: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        '''(experimental) Turn this Token into JSON.

        Called automatically when JSON.stringify() is called on a Token.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))


class _LazyBaseProxy(LazyBase):
    @jsii.member(jsii_name="resolveLazy")
    def _resolve_lazy(self, context: IResolveContext) -> typing.Any:
        '''
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LazyBase._resolve_lazy)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveLazy", [context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, LazyBase).__jsii_proxy_class__ = lambda : _LazyBaseProxy


@jsii.data_type(
    jsii_type="cdktf.LazyListValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint", "omit_empty": "omitEmpty"},
)
class LazyListValueOptions:
    def __init__(
        self,
        *,
        display_hint: typing.Optional[builtins.str] = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for creating a lazy list token.

        :param display_hint: (experimental) Use the given name as a display hint. Default: - No hint
        :param omit_empty: (experimental) If the produced list is empty, return 'undefined' instead. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LazyListValueOptions.__init__)
            check_type(argname="argument display_hint", value=display_hint, expected_type=type_hints["display_hint"])
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
        self._values: typing.Dict[str, typing.Any] = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty

    @builtins.property
    def display_hint(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the given name as a display hint.

        :default: - No hint

        :stability: experimental
        '''
        result = self._values.get("display_hint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the produced list is empty, return 'undefined' instead.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyListValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.LazyStringValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint"},
)
class LazyStringValueOptions:
    def __init__(self, *, display_hint: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Options for creating a lazy string token.

        :param display_hint: (experimental) Use the given name as a display hint. Default: - No hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LazyStringValueOptions.__init__)
            check_type(argname="argument display_hint", value=display_hint, expected_type=type_hints["display_hint"])
        self._values: typing.Dict[str, typing.Any] = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the given name as a display hint.

        :default: - No hint

        :stability: experimental
        '''
        result = self._values.get("display_hint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyStringValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.LocalBackendProps",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "workspace_dir": "workspaceDir"},
)
class LocalBackendProps:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        workspace_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The local backend stores state on the local filesystem, locks that state using system APIs, and performs operations locally.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/local

        :param path: (experimental) Path where the state file is stored. Default: - defaults to terraform.${stackId}.tfstate
        :param workspace_dir: (experimental) (Optional) The path to non-default workspaces.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LocalBackendProps.__init__)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument workspace_dir", value=workspace_dir, expected_type=type_hints["workspace_dir"])
        self._values: typing.Dict[str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if workspace_dir is not None:
            self._values["workspace_dir"] = workspace_dir

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path where the state file is stored.

        :default: - defaults to terraform.${stackId}.tfstate

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to non-default workspaces.

        :stability: experimental
        '''
        result = self._values.get("workspace_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.LocalExecProvisioner",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "type": "type",
        "environment": "environment",
        "interpreter": "interpreter",
        "when": "when",
        "working_dir": "workingDir",
    },
)
class LocalExecProvisioner:
    def __init__(
        self,
        *,
        command: builtins.str,
        type: builtins.str,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        interpreter: typing.Optional[typing.Sequence[builtins.str]] = None,
        when: typing.Optional[builtins.str] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The local-exec provisioner invokes a local executable after a resource is created.

        This invokes a process on the machine running Terraform, not on the resource.

        See {@link https://www.terraform.io/language/resources/provisioners/local-exec local-exec}

        :param command: (experimental) This is the command to execute. It can be provided as a relative path to the current working directory or as an absolute path. It is evaluated in a shell, and can use environment variables or Terraform variables.
        :param type: 
        :param environment: (experimental) A record of key value pairs representing the environment of the executed command. It inherits the current process environment.
        :param interpreter: (experimental) If provided, this is a list of interpreter arguments used to execute the command. The first argument is the interpreter itself. It can be provided as a relative path to the current working directory or as an absolute path The remaining arguments are appended prior to the command. This allows building command lines of the form "/bin/bash", "-c", "echo foo". If interpreter is unspecified, sensible defaults will be chosen based on the system OS.
        :param when: (experimental) If provided, specifies when Terraform will execute the command. For example, when = destroy specifies that the provisioner will run when the associated resource is destroyed
        :param working_dir: (experimental) If provided, specifies the working directory where command will be executed. It can be provided as a relative path to the current working directory or as an absolute path. The directory must exist.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LocalExecProvisioner.__init__)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
            check_type(argname="argument working_dir", value=working_dir, expected_type=type_hints["working_dir"])
        self._values: typing.Dict[str, typing.Any] = {
            "command": command,
            "type": type,
        }
        if environment is not None:
            self._values["environment"] = environment
        if interpreter is not None:
            self._values["interpreter"] = interpreter
        if when is not None:
            self._values["when"] = when
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def command(self) -> builtins.str:
        '''(experimental) This is the command to execute.

        It can be provided as a relative path to the current working directory or as an absolute path.
        It is evaluated in a shell, and can use environment variables or Terraform variables.

        :stability: experimental
        '''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A record of key value pairs representing the environment of the executed command.

        It inherits the current process environment.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def interpreter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) If provided, this is a list of interpreter arguments used to execute the command.

        The first argument is the interpreter itself.
        It can be provided as a relative path to the current working directory or as an absolute path
        The remaining arguments are appended prior to the command.
        This allows building command lines of the form "/bin/bash", "-c", "echo foo".
        If interpreter is unspecified, sensible defaults will be chosen based on the system OS.

        :stability: experimental
        '''
        result = self._values.get("interpreter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def when(self) -> typing.Optional[builtins.str]:
        '''(experimental) If provided, specifies when Terraform will execute the command.

        For example, when = destroy specifies that the provisioner will run when the associated resource is destroyed

        :stability: experimental
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) If provided, specifies the working directory where command will be executed.

        It can be provided as a relative path to the current working directory or as an absolute path.
        The directory must exist.

        :stability: experimental
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalExecProvisioner(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IManifest)
class Manifest(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Manifest"):
    '''
    :stability: experimental
    '''

    def __init__(self, version: builtins.str, outdir: builtins.str) -> None:
        '''
        :param version: -
        :param outdir: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Manifest.__init__)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
        jsii.create(self.__class__, self, [version, outdir])

    @jsii.member(jsii_name="buildManifest")
    def build_manifest(self) -> IManifest:
        '''
        :stability: experimental
        '''
        return typing.cast(IManifest, jsii.invoke(self, "buildManifest", []))

    @jsii.member(jsii_name="forStack")
    def for_stack(self, stack: "TerraformStack") -> "StackManifest":
        '''
        :param stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Manifest.for_stack)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast("StackManifest", jsii.invoke(self, "forStack", [stack]))

    @jsii.member(jsii_name="writeToFile")
    def write_to_file(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "writeToFile", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="fileName")
    def FILE_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "fileName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="stackFileName")
    def STACK_FILE_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "stackFileName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="stacksFolder")
    def STACKS_FOLDER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "stacksFolder"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.Mapping[builtins.str, "StackManifest"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "StackManifest"], jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.data_type(
    jsii_type="cdktf.MantaBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "key_id": "keyId",
        "path": "path",
        "insecure_skip_tls_verify": "insecureSkipTlsVerify",
        "key_material": "keyMaterial",
        "object_name": "objectName",
        "url": "url",
        "user": "user",
    },
)
class MantaBackendProps:
    def __init__(
        self,
        *,
        account: builtins.str,
        key_id: builtins.str,
        path: builtins.str,
        insecure_skip_tls_verify: typing.Optional[builtins.bool] = None,
        key_material: typing.Optional[builtins.str] = None,
        object_name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: 
        :param key_id: 
        :param path: 
        :param insecure_skip_tls_verify: 
        :param key_material: 
        :param object_name: 
        :param url: 
        :param user: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MantaBackendProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument insecure_skip_tls_verify", value=insecure_skip_tls_verify, expected_type=type_hints["insecure_skip_tls_verify"])
            check_type(argname="argument key_material", value=key_material, expected_type=type_hints["key_material"])
            check_type(argname="argument object_name", value=object_name, expected_type=type_hints["object_name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "key_id": key_id,
            "path": path,
        }
        if insecure_skip_tls_verify is not None:
            self._values["insecure_skip_tls_verify"] = insecure_skip_tls_verify
        if key_material is not None:
            self._values["key_material"] = key_material
        if object_name is not None:
            self._values["object_name"] = object_name
        if url is not None:
            self._values["url"] = url
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def account(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("key_id")
        assert result is not None, "Required property 'key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def insecure_skip_tls_verify(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("insecure_skip_tls_verify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_material(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("object_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MantaBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NamedCloudWorkspace(
    CloudWorkspace,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.NamedCloudWorkspace",
):
    '''(experimental) The name of a single Terraform Cloud workspace.

    You will only be able to use the workspace specified in the configuration with this working directory, and cannot manage workspaces from the CLI (e.g. terraform workspace select or terraform workspace new).

    :stability: experimental
    '''

    def __init__(self, name: builtins.str) -> None:
        '''
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NamedCloudWorkspace.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        jsii.create(self.__class__, self, [name])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(NamedCloudWorkspace, "name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.implements(IRemoteWorkspace)
class NamedRemoteWorkspace(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.NamedRemoteWorkspace",
):
    '''
    :stability: experimental
    '''

    def __init__(self, name: builtins.str) -> None:
        '''
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NamedRemoteWorkspace.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        jsii.create(self.__class__, self, [name])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(NamedRemoteWorkspace, "name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.implements(ITerraformAddressable, IResolvable)
class NumberMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.NumberMap"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NumberMap.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: builtins.str) -> jsii.Number:
        '''
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NumberMap.lookup)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(jsii.Number, jsii.invoke(self, "lookup", [key]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NumberMap.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(NumberMap, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(NumberMap, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)


@jsii.implements(ITerraformAddressable, IInterpolatingParent, IResolvable)
class NumberMapList(metaclass=jsii.JSIIMeta, jsii_type="cdktf.NumberMapList"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -
        :param wraps_set: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NumberMapList.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> NumberMap:
        '''
        :param index: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NumberMapList.get)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast(NumberMap, jsii.invoke(self, "get", [index]))

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, property: builtins.str) -> IResolvable:
        '''
        :param property: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NumberMapList.interpolation_for_attribute)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [property]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NumberMapList.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(NumberMapList, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(NumberMapList, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(NumberMapList, "_wraps_set").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.data_type(
    jsii_type="cdktf.OssAssumeRole",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "policy": "policy",
        "session_expiration": "sessionExpiration",
        "session_name": "sessionName",
    },
)
class OssAssumeRole:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        policy: typing.Optional[builtins.str] = None,
        session_expiration: typing.Optional[jsii.Number] = None,
        session_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: 
        :param policy: 
        :param session_expiration: 
        :param session_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OssAssumeRole.__init__)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument session_expiration", value=session_expiration, expected_type=type_hints["session_expiration"])
            check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "role_arn": role_arn,
        }
        if policy is not None:
            self._values["policy"] = policy
        if session_expiration is not None:
            self._values["session_expiration"] = session_expiration
        if session_name is not None:
            self._values["session_name"] = session_name

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_expiration(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("session_expiration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OssAssumeRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.OssBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "access_key": "accessKey",
        "acl": "acl",
        "assume_role": "assumeRole",
        "ecs_role_name": "ecsRoleName",
        "encrypt": "encrypt",
        "endpoint": "endpoint",
        "key": "key",
        "prefix": "prefix",
        "profile": "profile",
        "region": "region",
        "secret_key": "secretKey",
        "security_token": "securityToken",
        "shared_credentials_file": "sharedCredentialsFile",
        "tablestore_endpoint": "tablestoreEndpoint",
        "tablestore_table": "tablestoreTable",
    },
)
class OssBackendProps:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        assume_role: typing.Optional[typing.Union[OssAssumeRole, typing.Dict[str, typing.Any]]] = None,
        ecs_role_name: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        security_token: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        tablestore_endpoint: typing.Optional[builtins.str] = None,
        tablestore_table: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: 
        :param access_key: 
        :param acl: 
        :param assume_role: 
        :param ecs_role_name: 
        :param encrypt: 
        :param endpoint: 
        :param key: 
        :param prefix: 
        :param profile: 
        :param region: 
        :param secret_key: 
        :param security_token: 
        :param shared_credentials_file: 
        :param tablestore_endpoint: 
        :param tablestore_table: 

        :stability: experimental
        '''
        if isinstance(assume_role, dict):
            assume_role = OssAssumeRole(**assume_role)
        if __debug__:
            type_hints = typing.get_type_hints(OssBackendProps.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument assume_role", value=assume_role, expected_type=type_hints["assume_role"])
            check_type(argname="argument ecs_role_name", value=ecs_role_name, expected_type=type_hints["ecs_role_name"])
            check_type(argname="argument encrypt", value=encrypt, expected_type=type_hints["encrypt"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument security_token", value=security_token, expected_type=type_hints["security_token"])
            check_type(argname="argument shared_credentials_file", value=shared_credentials_file, expected_type=type_hints["shared_credentials_file"])
            check_type(argname="argument tablestore_endpoint", value=tablestore_endpoint, expected_type=type_hints["tablestore_endpoint"])
            check_type(argname="argument tablestore_table", value=tablestore_table, expected_type=type_hints["tablestore_table"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if ecs_role_name is not None:
            self._values["ecs_role_name"] = ecs_role_name
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if security_token is not None:
            self._values["security_token"] = security_token
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if tablestore_endpoint is not None:
            self._values["tablestore_endpoint"] = tablestore_endpoint
        if tablestore_table is not None:
            self._values["tablestore_table"] = tablestore_table

    @builtins.property
    def bucket(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role(self) -> typing.Optional[OssAssumeRole]:
        '''
        :stability: experimental
        '''
        result = self._values.get("assume_role")
        return typing.cast(typing.Optional[OssAssumeRole], result)

    @builtins.property
    def ecs_role_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ecs_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypt(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("encrypt")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("shared_credentials_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tablestore_endpoint(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tablestore_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tablestore_table(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tablestore_table")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OssBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.PgBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "conn_str": "connStr",
        "schema_name": "schemaName",
        "skip_schema_creation": "skipSchemaCreation",
    },
)
class PgBackendProps:
    def __init__(
        self,
        *,
        conn_str: builtins.str,
        schema_name: typing.Optional[builtins.str] = None,
        skip_schema_creation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param conn_str: 
        :param schema_name: 
        :param skip_schema_creation: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PgBackendProps.__init__)
            check_type(argname="argument conn_str", value=conn_str, expected_type=type_hints["conn_str"])
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument skip_schema_creation", value=skip_schema_creation, expected_type=type_hints["skip_schema_creation"])
        self._values: typing.Dict[str, typing.Any] = {
            "conn_str": conn_str,
        }
        if schema_name is not None:
            self._values["schema_name"] = schema_name
        if skip_schema_creation is not None:
            self._values["skip_schema_creation"] = skip_schema_creation

    @builtins.property
    def conn_str(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("conn_str")
        assert result is not None, "Required property 'conn_str' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_schema_creation(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_schema_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PgBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRemoteWorkspace)
class PrefixedRemoteWorkspaces(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.PrefixedRemoteWorkspaces",
):
    '''
    :stability: experimental
    '''

    def __init__(self, prefix: builtins.str) -> None:
        '''
        :param prefix: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PrefixedRemoteWorkspaces.__init__)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        jsii.create(self.__class__, self, [prefix])

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(PrefixedRemoteWorkspaces, "prefix").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="cdktf.RemoteBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "organization": "organization",
        "workspaces": "workspaces",
        "hostname": "hostname",
        "token": "token",
    },
)
class RemoteBackendProps:
    def __init__(
        self,
        *,
        organization: builtins.str,
        workspaces: IRemoteWorkspace,
        hostname: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteBackendProps.__init__)
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument workspaces", value=workspaces, expected_type=type_hints["workspaces"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[str, typing.Any] = {
            "organization": organization,
            "workspaces": workspaces,
        }
        if hostname is not None:
            self._values["hostname"] = hostname
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def organization(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspaces(self) -> IRemoteWorkspace:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspaces")
        assert result is not None, "Required property 'workspaces' is missing"
        return typing.cast(IRemoteWorkspace, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.RemoteExecProvisioner",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "connection": "connection",
        "inline": "inline",
        "script": "script",
        "scripts": "scripts",
    },
)
class RemoteExecProvisioner:
    def __init__(
        self,
        *,
        type: builtins.str,
        connection: typing.Optional[typing.Union[typing.Union["SSHProvisionerConnection", typing.Dict[str, typing.Any]], typing.Union["WinrmProvisionerConnection", typing.Dict[str, typing.Any]]]] = None,
        inline: typing.Optional[typing.Sequence[builtins.str]] = None,
        script: typing.Optional[builtins.str] = None,
        scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) The remote-exec provisioner invokes a script on a remote resource after it is created.

        This can be used to run a configuration management tool, bootstrap into a cluster, etc
        The remote-exec provisioner requires a connection and supports both ssh and winrm.

        See {@link https://www.terraform.io/language/resources/provisioners/remote-exec remote-exec}

        :param type: 
        :param connection: (experimental) Most provisioners require access to the remote resource via SSH or WinRM and expect a nested connection block with details about how to connect. A connection must be provided here or in the parent resource.
        :param inline: (experimental) This is a list of command strings. They are executed in the order they are provided. This cannot be provided with script or scripts.
        :param script: (experimental) This is a path (relative or absolute) to a local script that will be copied to the remote resource and then executed. This cannot be provided with inline or scripts.
        :param scripts: (experimental) This is a list of paths (relative or absolute) to local scripts that will be copied to the remote resource and then executed. They are executed in the order they are provided. This cannot be provided with inline or script.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteExecProvisioner.__init__)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if connection is not None:
            self._values["connection"] = connection
        if inline is not None:
            self._values["inline"] = inline
        if script is not None:
            self._values["script"] = script
        if scripts is not None:
            self._values["scripts"] = scripts

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union["SSHProvisionerConnection", "WinrmProvisionerConnection"]]:
        '''(experimental) Most provisioners require access to the remote resource via SSH or WinRM and expect a nested connection block with details about how to connect.

        A connection must be provided here or in the parent resource.

        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union["SSHProvisionerConnection", "WinrmProvisionerConnection"]], result)

    @builtins.property
    def inline(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) This is a list of command strings.

        They are executed in the order they are provided.
        This cannot be provided with script or scripts.

        :stability: experimental
        '''
        result = self._values.get("inline")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''(experimental) This is a path (relative or absolute) to a local script that will be copied to the remote resource and then executed.

        This cannot be provided with inline or scripts.

        :stability: experimental
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scripts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) This is a list of paths (relative or absolute) to local scripts that will be copied to the remote resource and then executed.

        They are executed in the order they are provided.
        This cannot be provided with inline or script.

        :stability: experimental
        '''
        result = self._values.get("scripts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteExecProvisioner(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.ResolveOptions",
    jsii_struct_bases=[],
    name_mapping={"resolver": "resolver", "scope": "scope", "preparing": "preparing"},
)
class ResolveOptions:
    def __init__(
        self,
        *,
        resolver: ITokenResolver,
        scope: constructs.IConstruct,
        preparing: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options to the resolve() operation.

        NOT the same as the ResolveContext; ResolveContext is exposed to Token
        implementors and resolution hooks, whereas this struct is just to bundle
        a number of things that would otherwise be arguments to resolve() in a
        readable way.

        :param resolver: (experimental) The resolver to apply to any resolvable tokens found.
        :param scope: (experimental) The scope from which resolution is performed.
        :param preparing: (experimental) Whether the resolution is being executed during the prepare phase or not. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ResolveOptions.__init__)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument preparing", value=preparing, expected_type=type_hints["preparing"])
        self._values: typing.Dict[str, typing.Any] = {
            "resolver": resolver,
            "scope": scope,
        }
        if preparing is not None:
            self._values["preparing"] = preparing

    @builtins.property
    def resolver(self) -> ITokenResolver:
        '''(experimental) The resolver to apply to any resolvable tokens found.

        :stability: experimental
        '''
        result = self._values.get("resolver")
        assert result is not None, "Required property 'resolver' is missing"
        return typing.cast(ITokenResolver, result)

    @builtins.property
    def scope(self) -> constructs.IConstruct:
        '''(experimental) The scope from which resolution is performed.

        :stability: experimental
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(constructs.IConstruct, result)

    @builtins.property
    def preparing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the resolution is being executed during the prepare phase or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("preparing")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolveOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IResource)
class Resource(
    constructs.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.Resource",
):
    '''(deprecated) A construct which represents a resource.

    :deprecated: - Please use Construct from the constructs package instead.

    :stability: deprecated
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Resource.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        '''(deprecated) The stack in which this resource is defined.

        :stability: deprecated
        '''
        return typing.cast("TerraformStack", jsii.get(self, "stack"))


class _ResourceProxy(Resource):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Resource).__jsii_proxy_class__ = lambda : _ResourceProxy


@jsii.data_type(
    jsii_type="cdktf.S3BackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "key": "key",
        "access_key": "accessKey",
        "acl": "acl",
        "assume_role_policy": "assumeRolePolicy",
        "assume_role_policy_arns": "assumeRolePolicyArns",
        "assume_role_tags": "assumeRoleTags",
        "assume_role_transitive_tag_keys": "assumeRoleTransitiveTagKeys",
        "dynamodb_endpoint": "dynamodbEndpoint",
        "dynamodb_table": "dynamodbTable",
        "encrypt": "encrypt",
        "endpoint": "endpoint",
        "external_id": "externalId",
        "force_path_style": "forcePathStyle",
        "iam_endpoint": "iamEndpoint",
        "kms_key_id": "kmsKeyId",
        "max_retries": "maxRetries",
        "profile": "profile",
        "region": "region",
        "role_arn": "roleArn",
        "secret_key": "secretKey",
        "session_name": "sessionName",
        "shared_credentials_file": "sharedCredentialsFile",
        "skip_credentials_validation": "skipCredentialsValidation",
        "skip_metadata_api_check": "skipMetadataApiCheck",
        "skip_region_validation": "skipRegionValidation",
        "sse_customer_key": "sseCustomerKey",
        "sts_endpoint": "stsEndpoint",
        "token": "token",
        "workspace_key_prefix": "workspaceKeyPrefix",
    },
)
class S3BackendProps:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        key: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        assume_role_policy: typing.Optional[builtins.str] = None,
        assume_role_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        assume_role_transitive_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        dynamodb_endpoint: typing.Optional[builtins.str] = None,
        dynamodb_table: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        force_path_style: typing.Optional[builtins.bool] = None,
        iam_endpoint: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        session_name: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        skip_credentials_validation: typing.Optional[builtins.bool] = None,
        skip_metadata_api_check: typing.Optional[builtins.bool] = None,
        skip_region_validation: typing.Optional[builtins.bool] = None,
        sse_customer_key: typing.Optional[builtins.str] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        workspace_key_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Stores the state as a given key in a given bucket on Amazon S3.

        This backend
        also supports state locking and consistency checking via Dynamo DB, which
        can be enabled by setting the dynamodb_table field to an existing DynamoDB
        table name. A single DynamoDB table can be used to lock multiple remote
        state files. Terraform generates key names that include the values of the
        bucket and key variables.

        Warning! It is highly recommended that you enable Bucket Versioning on the
        S3 bucket to allow for state recovery in the case of accidental deletions
        and human error.

        Read more about this backend in the Terraform docs:
        https://www.terraform.io/language/settings/backends/s3

        :param bucket: (experimental) Name of the S3 Bucket.
        :param key: (experimental) Path to the state file inside the S3 Bucket. When using a non-default workspace, the state path will be /workspace_key_prefix/workspace_name/key
        :param access_key: (experimental) (Optional) AWS access key. If configured, must also configure secret_key. This can also be sourced from the AWS_ACCESS_KEY_ID environment variable, AWS shared credentials file (e.g. ~/.aws/credentials), or AWS shared configuration file (e.g. ~/.aws/config).
        :param acl: (experimental) (Optional) Canned ACL to be applied to the state file.
        :param assume_role_policy: (experimental) (Optional) IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.
        :param assume_role_policy_arns: (experimental) (Optional) Set of Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.
        :param assume_role_tags: (experimental) (Optional) Map of assume role session tags.
        :param assume_role_transitive_tag_keys: (experimental) (Optional) Set of assume role session tag keys to pass to any subsequent sessions.
        :param dynamodb_endpoint: (experimental) (Optional) Custom endpoint for the AWS DynamoDB API. This can also be sourced from the AWS_DYNAMODB_ENDPOINT environment variable.
        :param dynamodb_table: (experimental) (Optional) Name of DynamoDB Table to use for state locking and consistency. The table must have a partition key named LockID with type of String. If not configured, state locking will be disabled.
        :param encrypt: (experimental) (Optional) Enable server side encryption of the state file.
        :param endpoint: (experimental) (Optional) Custom endpoint for the AWS S3 API. This can also be sourced from the AWS_S3_ENDPOINT environment variable.
        :param external_id: (experimental) (Optional) External identifier to use when assuming the role.
        :param force_path_style: (experimental) (Optional) Enable path-style S3 URLs (https:/// instead of https://.).
        :param iam_endpoint: (experimental) (Optional) Custom endpoint for the AWS Identity and Access Management (IAM) API. This can also be sourced from the AWS_IAM_ENDPOINT environment variable.
        :param kms_key_id: (experimental) (Optional) Amazon Resource Name (ARN) of a Key Management Service (KMS) Key to use for encrypting the state. Note that if this value is specified, Terraform will need kms:Encrypt, kms:Decrypt and kms:GenerateDataKey permissions on this KMS key.
        :param max_retries: (experimental) (Optional) The maximum number of times an AWS API request is retried on retryable failure. Defaults to 5.
        :param profile: (experimental) (Optional) Name of AWS profile in AWS shared credentials file (e.g. ~/.aws/credentials) or AWS shared configuration file (e.g. ~/.aws/config) to use for credentials and/or configuration. This can also be sourced from the AWS_PROFILE environment variable.
        :param region: (experimental) AWS Region of the S3 Bucket and DynamoDB Table (if used). This can also be sourced from the AWS_DEFAULT_REGION and AWS_REGION environment variables.
        :param role_arn: (experimental) (Optional) Amazon Resource Name (ARN) of the IAM Role to assume.
        :param secret_key: (experimental) (Optional) AWS secret access key. If configured, must also configure access_key. This can also be sourced from the AWS_SECRET_ACCESS_KEY environment variable, AWS shared credentials file (e.g. ~/.aws/credentials), or AWS shared configuration file (e.g. ~/.aws/config)
        :param session_name: (experimental) (Optional) Session name to use when assuming the role.
        :param shared_credentials_file: (experimental) (Optional) Path to the AWS shared credentials file. Defaults to ~/.aws/credentials.
        :param skip_credentials_validation: (experimental) (Optional) Skip credentials validation via the STS API.
        :param skip_metadata_api_check: (experimental) (Optional) Skip usage of EC2 Metadata API.
        :param skip_region_validation: (experimental) (Optional) Skip validation of provided region name.
        :param sse_customer_key: (experimental) (Optional) The key to use for encrypting state with Server-Side Encryption with Customer-Provided Keys (SSE-C). This is the base64-encoded value of the key, which must decode to 256 bits. This can also be sourced from the AWS_SSE_CUSTOMER_KEY environment variable, which is recommended due to the sensitivity of the value. Setting it inside a terraform file will cause it to be persisted to disk in terraform.tfstate.
        :param sts_endpoint: (experimental) (Optional) Custom endpoint for the AWS Security Token Service (STS) API. This can also be sourced from the AWS_STS_ENDPOINT environment variable.
        :param token: (experimental) (Optional) Multi-Factor Authentication (MFA) token. This can also be sourced from the AWS_SESSION_TOKEN environment variable.
        :param workspace_key_prefix: (experimental) (Optional) Prefix applied to the state path inside the bucket. This is only relevant when using a non-default workspace. Defaults to env:

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3BackendProps.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument assume_role_policy", value=assume_role_policy, expected_type=type_hints["assume_role_policy"])
            check_type(argname="argument assume_role_policy_arns", value=assume_role_policy_arns, expected_type=type_hints["assume_role_policy_arns"])
            check_type(argname="argument assume_role_tags", value=assume_role_tags, expected_type=type_hints["assume_role_tags"])
            check_type(argname="argument assume_role_transitive_tag_keys", value=assume_role_transitive_tag_keys, expected_type=type_hints["assume_role_transitive_tag_keys"])
            check_type(argname="argument dynamodb_endpoint", value=dynamodb_endpoint, expected_type=type_hints["dynamodb_endpoint"])
            check_type(argname="argument dynamodb_table", value=dynamodb_table, expected_type=type_hints["dynamodb_table"])
            check_type(argname="argument encrypt", value=encrypt, expected_type=type_hints["encrypt"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument force_path_style", value=force_path_style, expected_type=type_hints["force_path_style"])
            check_type(argname="argument iam_endpoint", value=iam_endpoint, expected_type=type_hints["iam_endpoint"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
            check_type(argname="argument shared_credentials_file", value=shared_credentials_file, expected_type=type_hints["shared_credentials_file"])
            check_type(argname="argument skip_credentials_validation", value=skip_credentials_validation, expected_type=type_hints["skip_credentials_validation"])
            check_type(argname="argument skip_metadata_api_check", value=skip_metadata_api_check, expected_type=type_hints["skip_metadata_api_check"])
            check_type(argname="argument skip_region_validation", value=skip_region_validation, expected_type=type_hints["skip_region_validation"])
            check_type(argname="argument sse_customer_key", value=sse_customer_key, expected_type=type_hints["sse_customer_key"])
            check_type(argname="argument sts_endpoint", value=sts_endpoint, expected_type=type_hints["sts_endpoint"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument workspace_key_prefix", value=workspace_key_prefix, expected_type=type_hints["workspace_key_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "key": key,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if assume_role_policy is not None:
            self._values["assume_role_policy"] = assume_role_policy
        if assume_role_policy_arns is not None:
            self._values["assume_role_policy_arns"] = assume_role_policy_arns
        if assume_role_tags is not None:
            self._values["assume_role_tags"] = assume_role_tags
        if assume_role_transitive_tag_keys is not None:
            self._values["assume_role_transitive_tag_keys"] = assume_role_transitive_tag_keys
        if dynamodb_endpoint is not None:
            self._values["dynamodb_endpoint"] = dynamodb_endpoint
        if dynamodb_table is not None:
            self._values["dynamodb_table"] = dynamodb_table
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if external_id is not None:
            self._values["external_id"] = external_id
        if force_path_style is not None:
            self._values["force_path_style"] = force_path_style
        if iam_endpoint is not None:
            self._values["iam_endpoint"] = iam_endpoint
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if session_name is not None:
            self._values["session_name"] = session_name
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if skip_credentials_validation is not None:
            self._values["skip_credentials_validation"] = skip_credentials_validation
        if skip_metadata_api_check is not None:
            self._values["skip_metadata_api_check"] = skip_metadata_api_check
        if skip_region_validation is not None:
            self._values["skip_region_validation"] = skip_region_validation
        if sse_customer_key is not None:
            self._values["sse_customer_key"] = sse_customer_key
        if sts_endpoint is not None:
            self._values["sts_endpoint"] = sts_endpoint
        if token is not None:
            self._values["token"] = token
        if workspace_key_prefix is not None:
            self._values["workspace_key_prefix"] = workspace_key_prefix

    @builtins.property
    def bucket(self) -> builtins.str:
        '''(experimental) Name of the S3 Bucket.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) Path to the state file inside the S3 Bucket.

        When using a non-default workspace, the state path will be /workspace_key_prefix/workspace_name/key

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) AWS access key.

        If configured, must also configure secret_key.
        This can also be sourced from
        the AWS_ACCESS_KEY_ID environment variable,
        AWS shared credentials file (e.g. ~/.aws/credentials),
        or AWS shared configuration file (e.g. ~/.aws/config).

        :stability: experimental
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Canned ACL to be applied to the state file.

        :stability: experimental
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role_policy(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.

        :stability: experimental
        '''
        result = self._values.get("assume_role_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) (Optional) Set of Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.

        :stability: experimental
        '''
        result = self._values.get("assume_role_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assume_role_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) (Optional) Map of assume role session tags.

        :stability: experimental
        '''
        result = self._values.get("assume_role_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def assume_role_transitive_tag_keys(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) (Optional) Set of assume role session tag keys to pass to any subsequent sessions.

        :stability: experimental
        '''
        result = self._values.get("assume_role_transitive_tag_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dynamodb_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Custom endpoint for the AWS DynamoDB API.

        This can also be sourced from the AWS_DYNAMODB_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("dynamodb_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb_table(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Name of DynamoDB Table to use for state locking and consistency.

        The table must have a partition key named LockID with type of String.
        If not configured, state locking will be disabled.

        :stability: experimental
        '''
        result = self._values.get("dynamodb_table")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypt(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Enable server side encryption of the state file.

        :stability: experimental
        '''
        result = self._values.get("encrypt")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Custom endpoint for the AWS S3 API.

        This can also be sourced from the AWS_S3_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) External identifier to use when assuming the role.

        :stability: experimental
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_path_style(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Enable path-style S3 URLs (https:/// instead of https://.).

        :stability: experimental
        '''
        result = self._values.get("force_path_style")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iam_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Custom endpoint for the AWS Identity and Access Management (IAM) API.

        This can also be sourced from the AWS_IAM_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("iam_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Amazon Resource Name (ARN) of a Key Management Service (KMS) Key to use for encrypting the state.

        Note that if this value is specified,
        Terraform will need kms:Encrypt, kms:Decrypt and kms:GenerateDataKey permissions on this KMS key.

        :stability: experimental
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''(experimental) (Optional) The maximum number of times an AWS API request is retried on retryable failure.

        Defaults to 5.

        :stability: experimental
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Name of AWS profile in AWS shared credentials file (e.g. ~/.aws/credentials) or AWS shared configuration file (e.g. ~/.aws/config) to use for credentials and/or configuration. This can also be sourced from the AWS_PROFILE environment variable.

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) AWS Region of the S3 Bucket and DynamoDB Table (if used).

        This can also
        be sourced from the AWS_DEFAULT_REGION and AWS_REGION environment
        variables.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Amazon Resource Name (ARN) of the IAM Role to assume.

        :stability: experimental
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) AWS secret access key.

        If configured, must also configure access_key.
        This can also be sourced from
        the AWS_SECRET_ACCESS_KEY environment variable,
        AWS shared credentials file (e.g. ~/.aws/credentials),
        or AWS shared configuration file (e.g. ~/.aws/config)

        :stability: experimental
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Session name to use when assuming the role.

        :stability: experimental
        '''
        result = self._values.get("session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Path to the AWS shared credentials file.

        Defaults to ~/.aws/credentials.

        :stability: experimental
        '''
        result = self._values.get("shared_credentials_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_credentials_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Skip credentials validation via the STS API.

        :stability: experimental
        '''
        result = self._values.get("skip_credentials_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skip_metadata_api_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Skip usage of EC2 Metadata API.

        :stability: experimental
        '''
        result = self._values.get("skip_metadata_api_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skip_region_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Skip validation of provided region name.

        :stability: experimental
        '''
        result = self._values.get("skip_region_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sse_customer_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The key to use for encrypting state with Server-Side Encryption with Customer-Provided Keys (SSE-C).

        This is the base64-encoded value of the key, which must decode to 256 bits.
        This can also be sourced from the AWS_SSE_CUSTOMER_KEY environment variable,
        which is recommended due to the sensitivity of the value.
        Setting it inside a terraform file will cause it to be persisted to disk in terraform.tfstate.

        :stability: experimental
        '''
        result = self._values.get("sse_customer_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Custom endpoint for the AWS Security Token Service (STS) API.

        This can also be sourced from the AWS_STS_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("sts_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Multi-Factor Authentication (MFA) token.

        This can also be sourced from the AWS_SESSION_TOKEN environment variable.

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_key_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Prefix applied to the state path inside the bucket.

        This is only relevant when using a non-default workspace. Defaults to env:

        :stability: experimental
        '''
        result = self._values.get("workspace_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.SSHProvisionerConnection",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "type": "type",
        "agent": "agent",
        "agent_identity": "agentIdentity",
        "bastion_certificate": "bastionCertificate",
        "bastion_host": "bastionHost",
        "bastion_host_key": "bastionHostKey",
        "bastion_password": "bastionPassword",
        "bastion_port": "bastionPort",
        "bastion_private_key": "bastionPrivateKey",
        "bastion_user": "bastionUser",
        "certificate": "certificate",
        "host_key": "hostKey",
        "password": "password",
        "port": "port",
        "private_key": "privateKey",
        "proxy_host": "proxyHost",
        "proxy_port": "proxyPort",
        "proxy_scheme": "proxyScheme",
        "proxy_user_name": "proxyUserName",
        "proxy_user_password": "proxyUserPassword",
        "script_path": "scriptPath",
        "target_platform": "targetPlatform",
        "timeout": "timeout",
        "user": "user",
    },
)
class SSHProvisionerConnection:
    def __init__(
        self,
        *,
        host: builtins.str,
        type: builtins.str,
        agent: typing.Optional[builtins.str] = None,
        agent_identity: typing.Optional[builtins.str] = None,
        bastion_certificate: typing.Optional[builtins.str] = None,
        bastion_host: typing.Optional[builtins.str] = None,
        bastion_host_key: typing.Optional[builtins.str] = None,
        bastion_password: typing.Optional[builtins.str] = None,
        bastion_port: typing.Optional[jsii.Number] = None,
        bastion_private_key: typing.Optional[builtins.str] = None,
        bastion_user: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        host_key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        private_key: typing.Optional[builtins.str] = None,
        proxy_host: typing.Optional[builtins.str] = None,
        proxy_port: typing.Optional[jsii.Number] = None,
        proxy_scheme: typing.Optional[builtins.str] = None,
        proxy_user_name: typing.Optional[builtins.str] = None,
        proxy_user_password: typing.Optional[builtins.str] = None,
        script_path: typing.Optional[builtins.str] = None,
        target_platform: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Most provisioners require access to the remote resource via SSH or WinRM and expect a nested connection block with details about how to connect.

        See {@link https://www.terraform.io/language/resources/provisioners/connection connection}

        :param host: (experimental) The address of the resource to connect to.
        :param type: (experimental) The connection type. Valid values are "ssh" and "winrm". Provisioners typically assume that the remote system runs Microsoft Windows when using WinRM. Behaviors based on the SSH target_platform will force Windows-specific behavior for WinRM, unless otherwise specified.
        :param agent: (experimental) Set to false to disable using ssh-agent to authenticate. On Windows the only supported SSH authentication agent is Pageant.
        :param agent_identity: (experimental) The preferred identity from the ssh agent for authentication.
        :param bastion_certificate: (experimental) The contents of a signed CA Certificate. The certificate argument must be used in conjunction with a bastion_private_key. These can be loaded from a file on disk using the the file function.
        :param bastion_host: (experimental) Setting this enables the bastion Host connection. The provisioner will connect to bastion_host first, and then connect from there to host.
        :param bastion_host_key: (experimental) The public key from the remote host or the signing CA, used to verify the host connection.
        :param bastion_password: (experimental) The password to use for the bastion host.
        :param bastion_port: (experimental) The port to use connect to the bastion host.
        :param bastion_private_key: (experimental) The contents of an SSH key file to use for the bastion host. These can be loaded from a file on disk using the file function.
        :param bastion_user: (experimental) The user for the connection to the bastion host.
        :param certificate: (experimental) The contents of a signed CA Certificate. The certificate argument must be used in conjunction with a private_key. These can be loaded from a file on disk using the the file function.
        :param host_key: (experimental) The public key from the remote host or the signing CA, used to verify the connection.
        :param password: (experimental) The password to use for the connection.
        :param port: (experimental) The port to connect to. Default: 22
        :param private_key: (experimental) The contents of an SSH key to use for the connection. These can be loaded from a file on disk using the file function. This takes preference over password if provided.
        :param proxy_host: (experimental) Setting this enables the SSH over HTTP connection. This host will be connected to first, and then the host or bastion_host connection will be made from there.
        :param proxy_port: (experimental) The port to use connect to the proxy host.
        :param proxy_scheme: (experimental) The ssh connection also supports the following fields to facilitate connections by SSH over HTTP proxy.
        :param proxy_user_name: (experimental) The username to use connect to the private proxy host. This argument should be specified only if authentication is required for the HTTP Proxy server.
        :param proxy_user_password: (experimental) The password to use connect to the private proxy host. This argument should be specified only if authentication is required for the HTTP Proxy server.
        :param script_path: (experimental) The path used to copy scripts meant for remote execution. Refer to {@link https://www.terraform.io/language/resources/provisioners/connection#how-provisioners-execute-remote-scripts How Provisioners Execute Remote Scripts below for more details}
        :param target_platform: (experimental) The target platform to connect to. Valid values are "windows" and "unix". If the platform is set to windows, the default script_path is c:\\windows\\temp\\terraform_%RAND%.cmd, assuming the SSH default shell is cmd.exe. If the SSH default shell is PowerShell, set script_path to "c:/windows/temp/terraform_%RAND%.ps1" Default: unix
        :param timeout: (experimental) The timeout to wait for the connection to become available. Should be provided as a string (e.g., "30s" or "5m".) Default: 5m
        :param user: (experimental) The user to use for the connection. Default: root

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SSHProvisionerConnection.__init__)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument agent_identity", value=agent_identity, expected_type=type_hints["agent_identity"])
            check_type(argname="argument bastion_certificate", value=bastion_certificate, expected_type=type_hints["bastion_certificate"])
            check_type(argname="argument bastion_host", value=bastion_host, expected_type=type_hints["bastion_host"])
            check_type(argname="argument bastion_host_key", value=bastion_host_key, expected_type=type_hints["bastion_host_key"])
            check_type(argname="argument bastion_password", value=bastion_password, expected_type=type_hints["bastion_password"])
            check_type(argname="argument bastion_port", value=bastion_port, expected_type=type_hints["bastion_port"])
            check_type(argname="argument bastion_private_key", value=bastion_private_key, expected_type=type_hints["bastion_private_key"])
            check_type(argname="argument bastion_user", value=bastion_user, expected_type=type_hints["bastion_user"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument host_key", value=host_key, expected_type=type_hints["host_key"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument proxy_host", value=proxy_host, expected_type=type_hints["proxy_host"])
            check_type(argname="argument proxy_port", value=proxy_port, expected_type=type_hints["proxy_port"])
            check_type(argname="argument proxy_scheme", value=proxy_scheme, expected_type=type_hints["proxy_scheme"])
            check_type(argname="argument proxy_user_name", value=proxy_user_name, expected_type=type_hints["proxy_user_name"])
            check_type(argname="argument proxy_user_password", value=proxy_user_password, expected_type=type_hints["proxy_user_password"])
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
            check_type(argname="argument target_platform", value=target_platform, expected_type=type_hints["target_platform"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[str, typing.Any] = {
            "host": host,
            "type": type,
        }
        if agent is not None:
            self._values["agent"] = agent
        if agent_identity is not None:
            self._values["agent_identity"] = agent_identity
        if bastion_certificate is not None:
            self._values["bastion_certificate"] = bastion_certificate
        if bastion_host is not None:
            self._values["bastion_host"] = bastion_host
        if bastion_host_key is not None:
            self._values["bastion_host_key"] = bastion_host_key
        if bastion_password is not None:
            self._values["bastion_password"] = bastion_password
        if bastion_port is not None:
            self._values["bastion_port"] = bastion_port
        if bastion_private_key is not None:
            self._values["bastion_private_key"] = bastion_private_key
        if bastion_user is not None:
            self._values["bastion_user"] = bastion_user
        if certificate is not None:
            self._values["certificate"] = certificate
        if host_key is not None:
            self._values["host_key"] = host_key
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if private_key is not None:
            self._values["private_key"] = private_key
        if proxy_host is not None:
            self._values["proxy_host"] = proxy_host
        if proxy_port is not None:
            self._values["proxy_port"] = proxy_port
        if proxy_scheme is not None:
            self._values["proxy_scheme"] = proxy_scheme
        if proxy_user_name is not None:
            self._values["proxy_user_name"] = proxy_user_name
        if proxy_user_password is not None:
            self._values["proxy_user_password"] = proxy_user_password
        if script_path is not None:
            self._values["script_path"] = script_path
        if target_platform is not None:
            self._values["target_platform"] = target_platform
        if timeout is not None:
            self._values["timeout"] = timeout
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def host(self) -> builtins.str:
        '''(experimental) The address of the resource to connect to.

        :stability: experimental
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) The connection type.

        Valid values are "ssh" and "winrm".
        Provisioners typically assume that the remote system runs Microsoft Windows when using WinRM.
        Behaviors based on the SSH target_platform will force Windows-specific behavior for WinRM, unless otherwise specified.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent(self) -> typing.Optional[builtins.str]:
        '''(experimental) Set to false to disable using ssh-agent to authenticate.

        On Windows the only supported SSH authentication agent is Pageant.

        :stability: experimental
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_identity(self) -> typing.Optional[builtins.str]:
        '''(experimental) The preferred identity from the ssh agent for authentication.

        :stability: experimental
        '''
        result = self._values.get("agent_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bastion_certificate(self) -> typing.Optional[builtins.str]:
        '''(experimental) The contents of a signed CA Certificate.

        The certificate argument must be used in conjunction with a bastion_private_key.
        These can be loaded from a file on disk using the the file function.

        :stability: experimental
        '''
        result = self._values.get("bastion_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bastion_host(self) -> typing.Optional[builtins.str]:
        '''(experimental) Setting this enables the bastion Host connection.

        The provisioner will connect to bastion_host first, and then connect from there to host.

        :stability: experimental
        '''
        result = self._values.get("bastion_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bastion_host_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The public key from the remote host or the signing CA, used to verify the host connection.

        :stability: experimental
        '''
        result = self._values.get("bastion_host_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bastion_password(self) -> typing.Optional[builtins.str]:
        '''(experimental) The password to use for the bastion host.

        :stability: experimental
        '''
        result = self._values.get("bastion_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bastion_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port to use connect to the bastion host.

        :stability: experimental
        '''
        result = self._values.get("bastion_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bastion_private_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The contents of an SSH key file to use for the bastion host.

        These can be loaded from a file on disk using the file function.

        :stability: experimental
        '''
        result = self._values.get("bastion_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bastion_user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user for the connection to the bastion host.

        :stability: experimental
        '''
        result = self._values.get("bastion_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''(experimental) The contents of a signed CA Certificate.

        The certificate argument must be used in conjunction with a private_key.
        These can be loaded from a file on disk using the the file function.

        :stability: experimental
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The public key from the remote host or the signing CA, used to verify the connection.

        :stability: experimental
        '''
        result = self._values.get("host_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) The password to use for the connection.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port to connect to.

        :default: 22

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The contents of an SSH key to use for the connection.

        These can be loaded from a file on disk using the file function.
        This takes preference over password if provided.

        :stability: experimental
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_host(self) -> typing.Optional[builtins.str]:
        '''(experimental) Setting this enables the SSH over HTTP connection.

        This host will be connected to first, and then the host or bastion_host connection will be made from there.

        :stability: experimental
        '''
        result = self._values.get("proxy_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port to use connect to the proxy host.

        :stability: experimental
        '''
        result = self._values.get("proxy_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proxy_scheme(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ssh connection also supports the following fields to facilitate connections by SSH over HTTP proxy.

        :stability: experimental
        '''
        result = self._values.get("proxy_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_user_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The username to use connect to the private proxy host.

        This argument should be specified only if authentication is required for the HTTP Proxy server.

        :stability: experimental
        '''
        result = self._values.get("proxy_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_user_password(self) -> typing.Optional[builtins.str]:
        '''(experimental) The password to use connect to the private proxy host.

        This argument should be specified only if authentication is required for the HTTP Proxy server.

        :stability: experimental
        '''
        result = self._values.get("proxy_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path used to copy scripts meant for remote execution.

        Refer to {@link https://www.terraform.io/language/resources/provisioners/connection#how-provisioners-execute-remote-scripts How Provisioners Execute Remote Scripts below for more details}

        :stability: experimental
        '''
        result = self._values.get("script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_platform(self) -> typing.Optional[builtins.str]:
        '''(experimental) The target platform to connect to.

        Valid values are "windows" and "unix".
        If the platform is set to windows, the default script_path is c:\\windows\\temp\\terraform_%RAND%.cmd, assuming the SSH default shell is cmd.exe.
        If the SSH default shell is PowerShell, set script_path to "c:/windows/temp/terraform_%RAND%.ps1"

        :default: unix

        :stability: experimental
        '''
        result = self._values.get("target_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''(experimental) The timeout to wait for the connection to become available.

        Should be provided as a string (e.g., "30s" or "5m".)

        :default: 5m

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user to use for the connection.

        :default: root

        :stability: experimental
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SSHProvisionerConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.StackAnnotation",
    jsii_struct_bases=[],
    name_mapping={
        "construct_path": "constructPath",
        "level": "level",
        "message": "message",
        "stacktrace": "stacktrace",
    },
)
class StackAnnotation:
    def __init__(
        self,
        *,
        construct_path: builtins.str,
        level: AnnotationMetadataEntryType,
        message: builtins.str,
        stacktrace: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param construct_path: 
        :param level: 
        :param message: 
        :param stacktrace: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StackAnnotation.__init__)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument stacktrace", value=stacktrace, expected_type=type_hints["stacktrace"])
        self._values: typing.Dict[str, typing.Any] = {
            "construct_path": construct_path,
            "level": level,
            "message": message,
        }
        if stacktrace is not None:
            self._values["stacktrace"] = stacktrace

    @builtins.property
    def construct_path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("construct_path")
        assert result is not None, "Required property 'construct_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def level(self) -> AnnotationMetadataEntryType:
        '''
        :stability: experimental
        '''
        result = self._values.get("level")
        assert result is not None, "Required property 'level' is missing"
        return typing.cast(AnnotationMetadataEntryType, result)

    @builtins.property
    def message(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stacktrace(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stacktrace")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackAnnotation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.StackManifest",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "construct_path": "constructPath",
        "dependencies": "dependencies",
        "name": "name",
        "synthesized_stack_path": "synthesizedStackPath",
        "working_directory": "workingDirectory",
    },
)
class StackManifest:
    def __init__(
        self,
        *,
        annotations: typing.Sequence[typing.Union[StackAnnotation, typing.Dict[str, typing.Any]]],
        construct_path: builtins.str,
        dependencies: typing.Sequence[builtins.str],
        name: builtins.str,
        synthesized_stack_path: builtins.str,
        working_directory: builtins.str,
    ) -> None:
        '''
        :param annotations: 
        :param construct_path: 
        :param dependencies: 
        :param name: 
        :param synthesized_stack_path: 
        :param working_directory: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StackManifest.__init__)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument synthesized_stack_path", value=synthesized_stack_path, expected_type=type_hints["synthesized_stack_path"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[str, typing.Any] = {
            "annotations": annotations,
            "construct_path": construct_path,
            "dependencies": dependencies,
            "name": name,
            "synthesized_stack_path": synthesized_stack_path,
            "working_directory": working_directory,
        }

    @builtins.property
    def annotations(self) -> typing.List[StackAnnotation]:
        '''
        :stability: experimental
        '''
        result = self._values.get("annotations")
        assert result is not None, "Required property 'annotations' is missing"
        return typing.cast(typing.List[StackAnnotation], result)

    @builtins.property
    def construct_path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("construct_path")
        assert result is not None, "Required property 'construct_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dependencies(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("dependencies")
        assert result is not None, "Required property 'dependencies' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def synthesized_stack_path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("synthesized_stack_path")
        assert result is not None, "Required property 'synthesized_stack_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def working_directory(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("working_directory")
        assert result is not None, "Required property 'working_directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IFragmentConcatenator)
class StringConcat(metaclass=jsii.JSIIMeta, jsii_type="cdktf.StringConcat"):
    '''(experimental) Converts all fragments to strings and concats those.

    Drops 'undefined's.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        '''(experimental) Concatenates string fragments.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StringConcat.join)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast(typing.Any, jsii.invoke(self, "join", [left, right]))


@jsii.implements(ITerraformAddressable, IResolvable)
class StringMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.StringMap"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StringMap.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: builtins.str) -> builtins.str:
        '''
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StringMap.lookup)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(builtins.str, jsii.invoke(self, "lookup", [key]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StringMap.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(StringMap, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(StringMap, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)


@jsii.implements(ITerraformAddressable, IInterpolatingParent, IResolvable)
class StringMapList(metaclass=jsii.JSIIMeta, jsii_type="cdktf.StringMapList"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -
        :param wraps_set: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StringMapList.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> StringMap:
        '''
        :param index: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StringMapList.get)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast(StringMap, jsii.invoke(self, "get", [index]))

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, property: builtins.str) -> IResolvable:
        '''
        :param property: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StringMapList.interpolation_for_attribute)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [property]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StringMapList.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(StringMapList, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(StringMapList, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(StringMapList, "_wraps_set").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.data_type(
    jsii_type="cdktf.SwiftBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "application_credential_id": "applicationCredentialId",
        "application_credential_name": "applicationCredentialName",
        "application_credential_secret": "applicationCredentialSecret",
        "archive_container": "archiveContainer",
        "auth_url": "authUrl",
        "cacert_file": "cacertFile",
        "cert": "cert",
        "cloud": "cloud",
        "default_domain": "defaultDomain",
        "domain_id": "domainId",
        "domain_name": "domainName",
        "expire_after": "expireAfter",
        "insecure": "insecure",
        "key": "key",
        "password": "password",
        "project_domain_id": "projectDomainId",
        "project_domain_name": "projectDomainName",
        "region_name": "regionName",
        "state_name": "stateName",
        "tenant_id": "tenantId",
        "tenant_name": "tenantName",
        "token": "token",
        "user_domain_id": "userDomainId",
        "user_domain_name": "userDomainName",
        "user_id": "userId",
        "user_name": "userName",
    },
)
class SwiftBackendProps:
    def __init__(
        self,
        *,
        container: builtins.str,
        application_credential_id: typing.Optional[builtins.str] = None,
        application_credential_name: typing.Optional[builtins.str] = None,
        application_credential_secret: typing.Optional[builtins.str] = None,
        archive_container: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        default_domain: typing.Optional[builtins.str] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        expire_after: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        project_domain_id: typing.Optional[builtins.str] = None,
        project_domain_name: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        state_name: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_domain_id: typing.Optional[builtins.str] = None,
        user_domain_name: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container: 
        :param application_credential_id: 
        :param application_credential_name: 
        :param application_credential_secret: 
        :param archive_container: 
        :param auth_url: 
        :param cacert_file: 
        :param cert: 
        :param cloud: 
        :param default_domain: 
        :param domain_id: 
        :param domain_name: 
        :param expire_after: 
        :param insecure: 
        :param key: 
        :param password: 
        :param project_domain_id: 
        :param project_domain_name: 
        :param region_name: 
        :param state_name: 
        :param tenant_id: 
        :param tenant_name: 
        :param token: 
        :param user_domain_id: 
        :param user_domain_name: 
        :param user_id: 
        :param user_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SwiftBackendProps.__init__)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument application_credential_id", value=application_credential_id, expected_type=type_hints["application_credential_id"])
            check_type(argname="argument application_credential_name", value=application_credential_name, expected_type=type_hints["application_credential_name"])
            check_type(argname="argument application_credential_secret", value=application_credential_secret, expected_type=type_hints["application_credential_secret"])
            check_type(argname="argument archive_container", value=archive_container, expected_type=type_hints["archive_container"])
            check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
            check_type(argname="argument cacert_file", value=cacert_file, expected_type=type_hints["cacert_file"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument cloud", value=cloud, expected_type=type_hints["cloud"])
            check_type(argname="argument default_domain", value=default_domain, expected_type=type_hints["default_domain"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument expire_after", value=expire_after, expected_type=type_hints["expire_after"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument project_domain_id", value=project_domain_id, expected_type=type_hints["project_domain_id"])
            check_type(argname="argument project_domain_name", value=project_domain_name, expected_type=type_hints["project_domain_name"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument state_name", value=state_name, expected_type=type_hints["state_name"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument tenant_name", value=tenant_name, expected_type=type_hints["tenant_name"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument user_domain_id", value=user_domain_id, expected_type=type_hints["user_domain_id"])
            check_type(argname="argument user_domain_name", value=user_domain_name, expected_type=type_hints["user_domain_name"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "container": container,
        }
        if application_credential_id is not None:
            self._values["application_credential_id"] = application_credential_id
        if application_credential_name is not None:
            self._values["application_credential_name"] = application_credential_name
        if application_credential_secret is not None:
            self._values["application_credential_secret"] = application_credential_secret
        if archive_container is not None:
            self._values["archive_container"] = archive_container
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if cacert_file is not None:
            self._values["cacert_file"] = cacert_file
        if cert is not None:
            self._values["cert"] = cert
        if cloud is not None:
            self._values["cloud"] = cloud
        if default_domain is not None:
            self._values["default_domain"] = default_domain
        if domain_id is not None:
            self._values["domain_id"] = domain_id
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if expire_after is not None:
            self._values["expire_after"] = expire_after
        if insecure is not None:
            self._values["insecure"] = insecure
        if key is not None:
            self._values["key"] = key
        if password is not None:
            self._values["password"] = password
        if project_domain_id is not None:
            self._values["project_domain_id"] = project_domain_id
        if project_domain_name is not None:
            self._values["project_domain_name"] = project_domain_name
        if region_name is not None:
            self._values["region_name"] = region_name
        if state_name is not None:
            self._values["state_name"] = state_name
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if tenant_name is not None:
            self._values["tenant_name"] = tenant_name
        if token is not None:
            self._values["token"] = token
        if user_domain_id is not None:
            self._values["user_domain_id"] = user_domain_id
        if user_domain_name is not None:
            self._values["user_domain_name"] = user_domain_name
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def container(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_credential_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("application_credential_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_credential_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("application_credential_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_credential_secret(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("application_credential_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def archive_container(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("archive_container")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cacert_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cacert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloud")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_domain(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expire_after(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("expire_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("project_domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("project_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("region_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("state_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tenant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SwiftBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaggedCloudWorkspaces(
    CloudWorkspace,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TaggedCloudWorkspaces",
):
    '''(experimental) A set of Terraform Cloud workspace tags.

    You will be able to use this working directory with any workspaces that have all of the specified tags, and can use the terraform workspace commands to switch between them or create new workspaces. New workspaces will automatically have the specified tags. This option conflicts with name.

    :stability: experimental
    '''

    def __init__(self, tags: typing.Sequence[builtins.str]) -> None:
        '''
        :param tags: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TaggedCloudWorkspaces.__init__)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        jsii.create(self.__class__, self, [tags])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TaggedCloudWorkspaces, "tags").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


class TerraformAsset(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformAsset",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        path: builtins.str,
        asset_hash: typing.Optional[builtins.str] = None,
        type: typing.Optional[AssetType] = None,
    ) -> None:
        '''(experimental) A Terraform Asset takes a file or directory outside of the CDK for Terraform context and moves it into it.

        Assets copy referenced files into the stacks context for further usage in other resources.

        :param scope: -
        :param id: -
        :param path: 
        :param asset_hash: 
        :param type: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformAsset.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TerraformAssetConfig(path=path, asset_hash=asset_hash, type=type)

        jsii.create(self.__class__, self, [scope, id, config])

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        '''(experimental) Name of the asset.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) The path relative to the root of the terraform directory in posix format Use this property to reference the asset.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="assetHash")
    def asset_hash(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetHash"))

    @asset_hash.setter
    def asset_hash(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformAsset, "asset_hash").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetHash", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> AssetType:
        '''
        :stability: experimental
        '''
        return typing.cast(AssetType, jsii.get(self, "type"))

    @type.setter
    def type(self, value: AssetType) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformAsset, "type").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="cdktf.TerraformAssetConfig",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "asset_hash": "assetHash", "type": "type"},
)
class TerraformAssetConfig:
    def __init__(
        self,
        *,
        path: builtins.str,
        asset_hash: typing.Optional[builtins.str] = None,
        type: typing.Optional[AssetType] = None,
    ) -> None:
        '''
        :param path: 
        :param asset_hash: 
        :param type: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformAssetConfig.__init__)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[str, typing.Any] = {
            "path": path,
        }
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[AssetType]:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[AssetType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformAssetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformElement(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformElement",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        element_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param element_type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformElement.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument element_type", value=element_type, expected_type=type_hints["element_type"])
        jsii.create(self.__class__, self, [scope, id, element_type])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: builtins.str, value: typing.Any) -> None:
        '''
        :param path: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformElement.add_override)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addOverride", [path, value]))

    @jsii.member(jsii_name="overrideLogicalId")
    def override_logical_id(self, new_logical_id: builtins.str) -> None:
        '''(experimental) Overrides the auto-generated logical ID with a specific ID.

        :param new_logical_id: The new logical ID to use for this stack element.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformElement.override_logical_id)
            check_type(argname="argument new_logical_id", value=new_logical_id, expected_type=type_hints["new_logical_id"])
        return typing.cast(None, jsii.invoke(self, "overrideLogicalId", [new_logical_id]))

    @jsii.member(jsii_name="resetOverrideLogicalId")
    def reset_override_logical_id(self) -> None:
        '''(experimental) Resets a previously passed logical Id to use the auto-generated logical id again.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetOverrideLogicalId", []))

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="cdktfStack")
    def cdktf_stack(self) -> "TerraformStack":
        '''
        :stability: experimental
        '''
        return typing.cast("TerraformStack", jsii.get(self, "cdktfStack"))

    @builtins.property
    @jsii.member(jsii_name="constructNodeMetadata")
    def _construct_node_metadata(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "constructNodeMetadata"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "friendlyUniqueId"))

    @builtins.property
    @jsii.member(jsii_name="rawOverrides")
    def _raw_overrides(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "rawOverrides"))


@jsii.data_type(
    jsii_type="cdktf.TerraformElementMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "stack_trace": "stackTrace",
        "unique_id": "uniqueId",
    },
)
class TerraformElementMetadata:
    def __init__(
        self,
        *,
        path: builtins.str,
        stack_trace: typing.Sequence[builtins.str],
        unique_id: builtins.str,
    ) -> None:
        '''
        :param path: 
        :param stack_trace: 
        :param unique_id: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformElementMetadata.__init__)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument stack_trace", value=stack_trace, expected_type=type_hints["stack_trace"])
            check_type(argname="argument unique_id", value=unique_id, expected_type=type_hints["unique_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "path": path,
            "stack_trace": stack_trace,
            "unique_id": unique_id,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_trace(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stack_trace")
        assert result is not None, "Required property 'stack_trace' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def unique_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("unique_id")
        assert result is not None, "Required property 'unique_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformElementMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITerraformIterator)
class TerraformIterator(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformIterator",
):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromList")
    @builtins.classmethod
    def from_list(
        cls,
        list: typing.Union[typing.Sequence[builtins.str], IResolvable, typing.Sequence[jsii.Number], "ComplexList", StringMapList, NumberMapList, "BooleanMapList", "AnyMapList", typing.Sequence[typing.Union[builtins.bool, IResolvable]]],
    ) -> "ListTerraformIterator":
        '''(experimental) Creates a new iterator from a list.

        :param list: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.from_list)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast("ListTerraformIterator", jsii.sinvoke(cls, "fromList", [list]))

    @jsii.member(jsii_name="fromMap")
    @builtins.classmethod
    def from_map(
        cls,
        map: typing.Union["ComplexMap", typing.Mapping[builtins.str, typing.Any], typing.Mapping[builtins.str, builtins.str], typing.Mapping[builtins.str, jsii.Number], typing.Mapping[builtins.str, builtins.bool]],
    ) -> "MapTerraformIterator":
        '''(experimental) Creates a new iterator from a map.

        :param map: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.from_map)
            check_type(argname="argument map", value=map, expected_type=type_hints["map"])
        return typing.cast("MapTerraformIterator", jsii.sinvoke(cls, "fromMap", [map]))

    @jsii.member(jsii_name="dynamic")
    def dynamic(
        self,
        attributes: typing.Mapping[builtins.str, typing.Any],
    ) -> IResolvable:
        '''
        :param attributes: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.dynamic)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
        return typing.cast(IResolvable, jsii.invoke(self, "dynamic", [attributes]))

    @jsii.member(jsii_name="getAny")
    def get_any(self, attribute: builtins.str) -> IResolvable:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as any

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_any)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "getAny", [attribute]))

    @jsii.member(jsii_name="getAnyMap")
    def get_any_map(
        self,
        attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a map of any

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_any_map)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "getAnyMap", [attribute]))

    @jsii.member(jsii_name="getBoolean")
    def get_boolean(self, attribute: builtins.str) -> IResolvable:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a boolean

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_boolean)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "getBoolean", [attribute]))

    @jsii.member(jsii_name="getBooleanMap")
    def get_boolean_map(
        self,
        attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.bool]:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a map of booleans

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_boolean_map)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.bool], jsii.invoke(self, "getBooleanMap", [attribute]))

    @jsii.member(jsii_name="getList")
    def get_list(self, attribute: builtins.str) -> typing.List[builtins.str]:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a (string) list

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_list)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getList", [attribute]))

    @jsii.member(jsii_name="getMap")
    def get_map(
        self,
        attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a map

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_map)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "getMap", [attribute]))

    @jsii.member(jsii_name="getNumber")
    def get_number(self, attribute: builtins.str) -> jsii.Number:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a number

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_number)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getNumber", [attribute]))

    @jsii.member(jsii_name="getNumberList")
    def get_number_list(self, attribute: builtins.str) -> typing.List[jsii.Number]:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a number list

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_number_list)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(typing.List[jsii.Number], jsii.invoke(self, "getNumberList", [attribute]))

    @jsii.member(jsii_name="getNumberMap")
    def get_number_map(
        self,
        attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, jsii.Number]:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a map of numbers

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_number_map)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.invoke(self, "getNumberMap", [attribute]))

    @jsii.member(jsii_name="getString")
    def get_string(self, attribute: builtins.str) -> builtins.str:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a string

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_string)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(builtins.str, jsii.invoke(self, "getString", [attribute]))

    @jsii.member(jsii_name="getStringMap")
    def get_string_map(
        self,
        attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :param attribute: name of the property to retrieve.

        :return: the given attribute of the current item iterated over as a map of strings

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformIterator.get_string_map)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "getStringMap", [attribute]))


class _TerraformIteratorProxy(TerraformIterator):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TerraformIterator).__jsii_proxy_class__ = lambda : _TerraformIteratorProxy


@jsii.implements(ITerraformAddressable)
class TerraformLocal(
    TerraformElement,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformLocal",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        expression: typing.Any,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param expression: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformLocal.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        jsii.create(self.__class__, self, [scope, id, expression])

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="asBoolean")
    def as_boolean(self) -> IResolvable:
        '''
        :stability: experimental
        '''
        return typing.cast(IResolvable, jsii.get(self, "asBoolean"))

    @builtins.property
    @jsii.member(jsii_name="asList")
    def as_list(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "asList"))

    @builtins.property
    @jsii.member(jsii_name="asNumber")
    def as_number(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "asNumber"))

    @builtins.property
    @jsii.member(jsii_name="asString")
    def as_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "asString"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformLocal, "expression").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value)


@jsii.data_type(
    jsii_type="cdktf.TerraformMetaArguments",
    jsii_struct_bases=[],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
    },
)
class TerraformMetaArguments:
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union["WinrmProvisionerConnection", typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union["TerraformResourceLifecycle", typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional["TerraformProvider"] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 

        :stability: experimental
        '''
        if isinstance(lifecycle, dict):
            lifecycle = TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(TerraformMetaArguments.__init__)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
        self._values: typing.Dict[str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[SSHProvisionerConnection, "WinrmProvisionerConnection"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[SSHProvisionerConnection, "WinrmProvisionerConnection"]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional["TerraformResourceLifecycle"], result)

    @builtins.property
    def provider(self) -> typing.Optional["TerraformProvider"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional["TerraformProvider"], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[FileProvisioner, LocalExecProvisioner, RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[FileProvisioner, LocalExecProvisioner, RemoteExecProvisioner]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformMetaArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITerraformDependable)
class TerraformModule(
    TerraformElement,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformModule",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        source: builtins.str,
        version: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union["TerraformProvider", typing.Union["TerraformModuleProvider", typing.Dict[str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source: 
        :param version: 
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformModule.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = TerraformModuleOptions(
            source=source,
            version=version,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, options])

    @jsii.member(jsii_name="addProvider")
    def add_provider(
        self,
        provider: typing.Union["TerraformProvider", typing.Union["TerraformModuleProvider", typing.Dict[str, typing.Any]]],
    ) -> None:
        '''
        :param provider: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformModule.add_provider)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(None, jsii.invoke(self, "addProvider", [provider]))

    @jsii.member(jsii_name="getString")
    def get_string(self, output: builtins.str) -> builtins.str:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformModule.get_string)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(builtins.str, jsii.invoke(self, "getString", [output]))

    @jsii.member(jsii_name="interpolationForOutput")
    def interpolation_for_output(self, module_output: builtins.str) -> IResolvable:
        '''
        :param module_output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformModule.interpolation_for_output)
            check_type(argname="argument module_output", value=module_output, expected_type=type_hints["module_output"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForOutput", [module_output]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="providers")
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union["TerraformProvider", "TerraformModuleProvider"]]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[typing.Union["TerraformProvider", "TerraformModuleProvider"]]], jsii.get(self, "providers"))

    @builtins.property
    @jsii.member(jsii_name="skipAssetCreationFromLocalModules")
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipAssetCreationFromLocalModules"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformModule, "depends_on").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="forEach")
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[ITerraformIterator], jsii.get(self, "forEach"))

    @for_each.setter
    def for_each(self, value: typing.Optional[ITerraformIterator]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformModule, "for_each").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forEach", value)


class _TerraformModuleProxy(TerraformModule):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TerraformModule).__jsii_proxy_class__ = lambda : _TerraformModuleProxy


@jsii.data_type(
    jsii_type="cdktf.TerraformModuleProvider",
    jsii_struct_bases=[],
    name_mapping={"module_alias": "moduleAlias", "provider": "provider"},
)
class TerraformModuleProvider:
    def __init__(
        self,
        *,
        module_alias: builtins.str,
        provider: "TerraformProvider",
    ) -> None:
        '''
        :param module_alias: 
        :param provider: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformModuleProvider.__init__)
            check_type(argname="argument module_alias", value=module_alias, expected_type=type_hints["module_alias"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        self._values: typing.Dict[str, typing.Any] = {
            "module_alias": module_alias,
            "provider": provider,
        }

    @builtins.property
    def module_alias(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("module_alias")
        assert result is not None, "Required property 'module_alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> "TerraformProvider":
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast("TerraformProvider", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformModuleProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.TerraformModuleUserOptions",
    jsii_struct_bases=[],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
    },
)
class TerraformModuleUserOptions:
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union["TerraformProvider", typing.Union[TerraformModuleProvider, typing.Dict[str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformModuleUserOptions.__init__)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
        self._values: typing.Dict[str, typing.Any] = {}
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union["TerraformProvider", TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union["TerraformProvider", TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformModuleUserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformOutput(
    TerraformElement,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformOutput",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        value: typing.Any,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        description: typing.Optional[builtins.str] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        static_id: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param value: 
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param static_id: (experimental) If set to true the synthesized Terraform Output will be named after the ``id`` passed to the constructor instead of the default (TerraformOutput.friendlyUniqueId). Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformOutput.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TerraformOutputConfig(
            value=value,
            depends_on=depends_on,
            description=description,
            sensitive=sensitive,
            static_id=static_id,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="isTerrafromOutput")
    @builtins.classmethod
    def is_terrafrom_output(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformOutput.is_terrafrom_output)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isTerrafromOutput", [x]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="staticId")
    def static_id(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "staticId"))

    @static_id.setter
    def static_id(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformOutput, "static_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticId", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @value.setter
    def value(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformOutput, "value").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[ITerraformDependable]], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(
        self,
        value: typing.Optional[typing.List[ITerraformDependable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformOutput, "depends_on").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformOutput, "description").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "sensitive"))

    @sensitive.setter
    def sensitive(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformOutput, "sensitive").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sensitive", value)


@jsii.data_type(
    jsii_type="cdktf.TerraformOutputConfig",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "depends_on": "dependsOn",
        "description": "description",
        "sensitive": "sensitive",
        "static_id": "staticId",
    },
)
class TerraformOutputConfig:
    def __init__(
        self,
        *,
        value: typing.Any,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        description: typing.Optional[builtins.str] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        static_id: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param value: 
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param static_id: (experimental) If set to true the synthesized Terraform Output will be named after the ``id`` passed to the constructor instead of the default (TerraformOutput.friendlyUniqueId). Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformOutputConfig.__init__)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument sensitive", value=sensitive, expected_type=type_hints["sensitive"])
            check_type(argname="argument static_id", value=static_id, expected_type=type_hints["static_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if description is not None:
            self._values["description"] = description
        if sensitive is not None:
            self._values["sensitive"] = sensitive
        if static_id is not None:
            self._values["static_id"] = static_id

    @builtins.property
    def value(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[ITerraformDependable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sensitive(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("sensitive")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def static_id(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If set to true the synthesized Terraform Output will be named after the ``id`` passed to the constructor instead of the default (TerraformOutput.friendlyUniqueId).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("static_id")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformProvider(
    TerraformElement,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformProvider",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        terraform_resource_type: builtins.str,
        terraform_generator_metadata: typing.Optional[typing.Union["TerraformProviderGeneratorMetadata", typing.Dict[str, typing.Any]]] = None,
        terraform_provider_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param terraform_provider_source: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformProvider.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TerraformProviderConfig(
            terraform_resource_type=terraform_resource_type,
            terraform_generator_metadata=terraform_generator_metadata,
            terraform_provider_source=terraform_provider_source,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''(experimental) Adds this resource to the terraform JSON output.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="metaAttributes")
    def meta_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "metaAttributes"))

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformResourceType"))

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional["TerraformProviderGeneratorMetadata"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["TerraformProviderGeneratorMetadata"], jsii.get(self, "terraformGeneratorMetadata"))

    @builtins.property
    @jsii.member(jsii_name="terraformProviderSource")
    def terraform_provider_source(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformProviderSource"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformProvider, "alias").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)


class _TerraformProviderProxy(TerraformProvider):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TerraformProvider).__jsii_proxy_class__ = lambda : _TerraformProviderProxy


@jsii.data_type(
    jsii_type="cdktf.TerraformProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "terraform_resource_type": "terraformResourceType",
        "terraform_generator_metadata": "terraformGeneratorMetadata",
        "terraform_provider_source": "terraformProviderSource",
    },
)
class TerraformProviderConfig:
    def __init__(
        self,
        *,
        terraform_resource_type: builtins.str,
        terraform_generator_metadata: typing.Optional[typing.Union["TerraformProviderGeneratorMetadata", typing.Dict[str, typing.Any]]] = None,
        terraform_provider_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param terraform_provider_source: 

        :stability: experimental
        '''
        if isinstance(terraform_generator_metadata, dict):
            terraform_generator_metadata = TerraformProviderGeneratorMetadata(**terraform_generator_metadata)
        if __debug__:
            type_hints = typing.get_type_hints(TerraformProviderConfig.__init__)
            check_type(argname="argument terraform_resource_type", value=terraform_resource_type, expected_type=type_hints["terraform_resource_type"])
            check_type(argname="argument terraform_generator_metadata", value=terraform_generator_metadata, expected_type=type_hints["terraform_generator_metadata"])
            check_type(argname="argument terraform_provider_source", value=terraform_provider_source, expected_type=type_hints["terraform_provider_source"])
        self._values: typing.Dict[str, typing.Any] = {
            "terraform_resource_type": terraform_resource_type,
        }
        if terraform_generator_metadata is not None:
            self._values["terraform_generator_metadata"] = terraform_generator_metadata
        if terraform_provider_source is not None:
            self._values["terraform_provider_source"] = terraform_provider_source

    @builtins.property
    def terraform_resource_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("terraform_resource_type")
        assert result is not None, "Required property 'terraform_resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional["TerraformProviderGeneratorMetadata"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("terraform_generator_metadata")
        return typing.cast(typing.Optional["TerraformProviderGeneratorMetadata"], result)

    @builtins.property
    def terraform_provider_source(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("terraform_provider_source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.TerraformProviderGeneratorMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "provider_name": "providerName",
        "provider_version": "providerVersion",
        "provider_version_constraint": "providerVersionConstraint",
    },
)
class TerraformProviderGeneratorMetadata:
    def __init__(
        self,
        *,
        provider_name: builtins.str,
        provider_version: typing.Optional[builtins.str] = None,
        provider_version_constraint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param provider_name: 
        :param provider_version: 
        :param provider_version_constraint: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformProviderGeneratorMetadata.__init__)
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument provider_version", value=provider_version, expected_type=type_hints["provider_version"])
            check_type(argname="argument provider_version_constraint", value=provider_version_constraint, expected_type=type_hints["provider_version_constraint"])
        self._values: typing.Dict[str, typing.Any] = {
            "provider_name": provider_name,
        }
        if provider_version is not None:
            self._values["provider_version"] = provider_version
        if provider_version_constraint is not None:
            self._values["provider_version_constraint"] = provider_version_constraint

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_version_constraint(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider_version_constraint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformProviderGeneratorMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITerraformAddressable)
class TerraformRemoteState(
    TerraformElement,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformRemoteState",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        backend: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backend: -
        :param defaults: 
        :param workspace: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformRemoteState.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
        config = DataTerraformRemoteStateConfig(defaults=defaults, workspace=workspace)

        jsii.create(self.__class__, self, [scope, id, backend, config])

    @jsii.member(jsii_name="get")
    def get(self, output: builtins.str) -> IResolvable:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformRemoteState.get)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(IResolvable, jsii.invoke(self, "get", [output]))

    @jsii.member(jsii_name="getBoolean")
    def get_boolean(self, output: builtins.str) -> IResolvable:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformRemoteState.get_boolean)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(IResolvable, jsii.invoke(self, "getBoolean", [output]))

    @jsii.member(jsii_name="getList")
    def get_list(self, output: builtins.str) -> typing.List[builtins.str]:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformRemoteState.get_list)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getList", [output]))

    @jsii.member(jsii_name="getNumber")
    def get_number(self, output: builtins.str) -> jsii.Number:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformRemoteState.get_number)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getNumber", [output]))

    @jsii.member(jsii_name="getString")
    def get_string(self, output: builtins.str) -> builtins.str:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformRemoteState.get_string)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(builtins.str, jsii.invoke(self, "getString", [output]))

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''(experimental) Adds this resource to the terraform JSON output.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))


class _TerraformRemoteStateProxy(TerraformRemoteState):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TerraformRemoteState).__jsii_proxy_class__ = lambda : _TerraformRemoteStateProxy


@jsii.implements(ITerraformResource, ITerraformDependable, IInterpolatingParent)
class TerraformResource(
    TerraformElement,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformResource",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        terraform_resource_type: builtins.str,
        terraform_generator_metadata: typing.Optional[typing.Union[TerraformProviderGeneratorMetadata, typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union["WinrmProvisionerConnection", typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union["TerraformResourceLifecycle", typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TerraformResourceConfig(
            terraform_resource_type=terraform_resource_type,
            terraform_generator_metadata=terraform_generator_metadata,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="getAnyMapAttribute")
    def get_any_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_any_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "getAnyMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: builtins.str) -> IResolvable:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_boolean_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "getBooleanAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getBooleanMapAttribute")
    def get_boolean_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.bool]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_boolean_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.bool], jsii.invoke(self, "getBooleanMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.List[builtins.str]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_list_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getListAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: builtins.str) -> jsii.Number:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_number_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getNumberAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberListAttribute")
    def get_number_list_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.List[jsii.Number]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_number_list_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.List[jsii.Number], jsii.invoke(self, "getNumberListAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberMapAttribute")
    def get_number_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, jsii.Number]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_number_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.invoke(self, "getNumberMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: builtins.str) -> builtins.str:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_string_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(builtins.str, jsii.invoke(self, "getStringAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getStringMapAttribute")
    def get_string_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.get_string_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "getStringMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> IResolvable:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResource.interpolation_for_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''(experimental) Adds this resource to the terraform JSON output.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="terraformMetaArguments")
    def terraform_meta_arguments(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "terraformMetaArguments"))

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformResourceType"))

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional[TerraformProviderGeneratorMetadata]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[TerraformProviderGeneratorMetadata], jsii.get(self, "terraformGeneratorMetadata"))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(
        self,
    ) -> typing.Optional[typing.Union[SSHProvisionerConnection, "WinrmProvisionerConnection"]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[SSHProvisionerConnection, "WinrmProvisionerConnection"]], jsii.get(self, "connection"))

    @connection.setter
    def connection(
        self,
        value: typing.Optional[typing.Union[SSHProvisionerConnection, "WinrmProvisionerConnection"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformResource, "connection").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connection", value)

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "count"))

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformResource, "count").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformResource, "depends_on").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="forEach")
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[ITerraformIterator], jsii.get(self, "forEach"))

    @for_each.setter
    def for_each(self, value: typing.Optional[ITerraformIterator]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformResource, "for_each").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forEach", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["TerraformResourceLifecycle"], jsii.get(self, "lifecycle"))

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformResource, "lifecycle").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional[TerraformProvider]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[TerraformProvider], jsii.get(self, "provider"))

    @provider.setter
    def provider(self, value: typing.Optional[TerraformProvider]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformResource, "provider").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provider", value)

    @builtins.property
    @jsii.member(jsii_name="provisioners")
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[FileProvisioner, LocalExecProvisioner, RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[typing.Union[FileProvisioner, LocalExecProvisioner, RemoteExecProvisioner]]], jsii.get(self, "provisioners"))

    @provisioners.setter
    def provisioners(
        self,
        value: typing.Optional[typing.List[typing.Union[FileProvisioner, LocalExecProvisioner, RemoteExecProvisioner]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformResource, "provisioners").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioners", value)


@jsii.data_type(
    jsii_type="cdktf.TerraformResourceConfig",
    jsii_struct_bases=[TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "terraform_resource_type": "terraformResourceType",
        "terraform_generator_metadata": "terraformGeneratorMetadata",
    },
)
class TerraformResourceConfig(TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union["WinrmProvisionerConnection", typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union["TerraformResourceLifecycle", typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
        terraform_resource_type: builtins.str,
        terraform_generator_metadata: typing.Optional[typing.Union[TerraformProviderGeneratorMetadata, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 

        :stability: experimental
        '''
        if isinstance(lifecycle, dict):
            lifecycle = TerraformResourceLifecycle(**lifecycle)
        if isinstance(terraform_generator_metadata, dict):
            terraform_generator_metadata = TerraformProviderGeneratorMetadata(**terraform_generator_metadata)
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResourceConfig.__init__)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument terraform_resource_type", value=terraform_resource_type, expected_type=type_hints["terraform_resource_type"])
            check_type(argname="argument terraform_generator_metadata", value=terraform_generator_metadata, expected_type=type_hints["terraform_generator_metadata"])
        self._values: typing.Dict[str, typing.Any] = {
            "terraform_resource_type": terraform_resource_type,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if terraform_generator_metadata is not None:
            self._values["terraform_generator_metadata"] = terraform_generator_metadata

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[SSHProvisionerConnection, "WinrmProvisionerConnection"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[SSHProvisionerConnection, "WinrmProvisionerConnection"]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional["TerraformResourceLifecycle"], result)

    @builtins.property
    def provider(self) -> typing.Optional[TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[FileProvisioner, LocalExecProvisioner, RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[FileProvisioner, LocalExecProvisioner, RemoteExecProvisioner]]], result)

    @builtins.property
    def terraform_resource_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("terraform_resource_type")
        assert result is not None, "Required property 'terraform_resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional[TerraformProviderGeneratorMetadata]:
        '''
        :stability: experimental
        '''
        result = self._values.get("terraform_generator_metadata")
        return typing.cast(typing.Optional[TerraformProviderGeneratorMetadata], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformResourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.TerraformResourceLifecycle",
    jsii_struct_bases=[],
    name_mapping={
        "create_before_destroy": "createBeforeDestroy",
        "ignore_changes": "ignoreChanges",
        "prevent_destroy": "preventDestroy",
    },
)
class TerraformResourceLifecycle:
    def __init__(
        self,
        *,
        create_before_destroy: typing.Optional[builtins.bool] = None,
        ignore_changes: typing.Optional[typing.Union[typing.Sequence[builtins.str], builtins.str]] = None,
        prevent_destroy: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param create_before_destroy: 
        :param ignore_changes: 
        :param prevent_destroy: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformResourceLifecycle.__init__)
            check_type(argname="argument create_before_destroy", value=create_before_destroy, expected_type=type_hints["create_before_destroy"])
            check_type(argname="argument ignore_changes", value=ignore_changes, expected_type=type_hints["ignore_changes"])
            check_type(argname="argument prevent_destroy", value=prevent_destroy, expected_type=type_hints["prevent_destroy"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create_before_destroy is not None:
            self._values["create_before_destroy"] = create_before_destroy
        if ignore_changes is not None:
            self._values["ignore_changes"] = ignore_changes
        if prevent_destroy is not None:
            self._values["prevent_destroy"] = prevent_destroy

    @builtins.property
    def create_before_destroy(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("create_before_destroy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_changes(
        self,
    ) -> typing.Optional[typing.Union[typing.List[builtins.str], builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ignore_changes")
        return typing.cast(typing.Optional[typing.Union[typing.List[builtins.str], builtins.str]], result)

    @builtins.property
    def prevent_destroy(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("prevent_destroy")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformResourceLifecycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformSelf(metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformSelf"):
    '''(experimental) Expressions in connection blocks cannot refer to their parent resource by name.

    References create dependencies, and referring to a resource by name within its own block would create a dependency cycle.
    Instead, expressions can use the self object, which represents the connection's parent resource and has all of that resource's attributes.
    For example, use self.public_ip to reference an aws_instance's public_ip attribute.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="getAny")
    @builtins.classmethod
    def get_any(cls, key: builtins.str) -> typing.Any:
        '''(experimental) Only usable within a connection block to reference the connections parent resource.

        Access a property on the resource like this: ``getAny("hostPort")``

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformSelf.get_any)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "getAny", [key]))

    @jsii.member(jsii_name="getNumber")
    @builtins.classmethod
    def get_number(cls, key: builtins.str) -> jsii.Number:
        '''(experimental) Only usable within a connection block to reference the connections parent resource.

        Access a property on the resource like this: ``getNumber("hostPort")``

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformSelf.get_number)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "getNumber", [key]))

    @jsii.member(jsii_name="getString")
    @builtins.classmethod
    def get_string(cls, key: builtins.str) -> builtins.str:
        '''(experimental) Only usable within a connection block to reference the connections parent resource.

        Access a property on the resource like this: ``getString("publicIp")``

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformSelf.get_string)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getString", [key]))


class TerraformStack(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformStack",
):
    '''
    :stability: experimental
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="isStack")
    @builtins.classmethod
    def is_stack(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.is_stack)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStack", [x]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: constructs.IConstruct) -> "TerraformStack":
        '''
        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.of)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast("TerraformStack", jsii.sinvoke(cls, "of", [construct]))

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, dependency: "TerraformStack") -> None:
        '''
        :param dependency: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.add_dependency)
            check_type(argname="argument dependency", value=dependency, expected_type=type_hints["dependency"])
        return typing.cast(None, jsii.invoke(self, "addDependency", [dependency]))

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: builtins.str, value: typing.Any) -> None:
        '''
        :param path: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.add_override)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addOverride", [path, value]))

    @jsii.member(jsii_name="allocateLogicalId")
    def _allocate_logical_id(
        self,
        tf_element: typing.Union[TerraformElement, constructs.Node],
    ) -> builtins.str:
        '''(experimental) Returns the naming scheme used to allocate logical IDs.

        By default, uses
        the ``HashedAddressingScheme`` but this method can be overridden to customize
        this behavior.

        :param tf_element: The element for which the logical ID is allocated.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack._allocate_logical_id)
            check_type(argname="argument tf_element", value=tf_element, expected_type=type_hints["tf_element"])
        return typing.cast(builtins.str, jsii.invoke(self, "allocateLogicalId", [tf_element]))

    @jsii.member(jsii_name="allProviders")
    def all_providers(self) -> typing.List[TerraformProvider]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[TerraformProvider], jsii.invoke(self, "allProviders", []))

    @jsii.member(jsii_name="dependsOn")
    def depends_on(self, stack: "TerraformStack") -> builtins.bool:
        '''
        :param stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.depends_on)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.bool, jsii.invoke(self, "dependsOn", [stack]))

    @jsii.member(jsii_name="ensureBackendExists")
    def ensure_backend_exists(self) -> "TerraformBackend":
        '''
        :stability: experimental
        '''
        return typing.cast("TerraformBackend", jsii.invoke(self, "ensureBackendExists", []))

    @jsii.member(jsii_name="getLogicalId")
    def get_logical_id(
        self,
        tf_element: typing.Union[TerraformElement, constructs.Node],
    ) -> builtins.str:
        '''
        :param tf_element: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.get_logical_id)
            check_type(argname="argument tf_element", value=tf_element, expected_type=type_hints["tf_element"])
        return typing.cast(builtins.str, jsii.invoke(self, "getLogicalId", [tf_element]))

    @jsii.member(jsii_name="prepareStack")
    def prepare_stack(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "prepareStack", []))

    @jsii.member(jsii_name="registerIncomingCrossStackReference")
    def register_incoming_cross_stack_reference(
        self,
        from_stack: "TerraformStack",
    ) -> TerraformRemoteState:
        '''
        :param from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.register_incoming_cross_stack_reference)
            check_type(argname="argument from_stack", value=from_stack, expected_type=type_hints["from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "registerIncomingCrossStackReference", [from_stack]))

    @jsii.member(jsii_name="registerOutgoingCrossStackReference")
    def register_outgoing_cross_stack_reference(
        self,
        identifier: builtins.str,
    ) -> TerraformOutput:
        '''
        :param identifier: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStack.register_outgoing_cross_stack_reference)
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
        return typing.cast(TerraformOutput, jsii.invoke(self, "registerOutgoingCrossStackReference", [identifier]))

    @jsii.member(jsii_name="runAllValidations")
    def run_all_validations(self) -> None:
        '''(experimental) Run all validations on the stack.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "runAllValidations", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["TerraformStack"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["TerraformStack"], jsii.get(self, "dependencies"))

    @dependencies.setter
    def dependencies(self, value: typing.List["TerraformStack"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformStack, "dependencies").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencies", value)

    @builtins.property
    @jsii.member(jsii_name="synthesizer")
    def synthesizer(self) -> IStackSynthesizer:
        '''
        :stability: experimental
        '''
        return typing.cast(IStackSynthesizer, jsii.get(self, "synthesizer"))

    @synthesizer.setter
    def synthesizer(self, value: IStackSynthesizer) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformStack, "synthesizer").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synthesizer", value)


@jsii.data_type(
    jsii_type="cdktf.TerraformStackMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "backend": "backend",
        "stack_name": "stackName",
        "version": "version",
    },
)
class TerraformStackMetadata:
    def __init__(
        self,
        *,
        backend: builtins.str,
        stack_name: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param backend: 
        :param stack_name: 
        :param version: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformStackMetadata.__init__)
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {
            "backend": backend,
            "stack_name": stack_name,
            "version": version,
        }

    @builtins.property
    def backend(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("backend")
        assert result is not None, "Required property 'backend' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformStackMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITerraformAddressable)
class TerraformVariable(
    TerraformElement,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformVariable",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        default: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[builtins.bool] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
        validation: typing.Optional[typing.Sequence[typing.Union["TerraformVariableValidationConfig", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param default: 
        :param description: 
        :param nullable: 
        :param sensitive: 
        :param type: (experimental) The type argument in a variable block allows you to restrict the type of value that will be accepted as the value for a variable. If no type constraint is set then a value of any type is accepted. While type constraints are optional, we recommend specifying them; they serve as easy reminders for users of the module, and allow Terraform to return a helpful error message if the wrong type is used. Type constraints are created from a mixture of type keywords and type constructors. The supported type keywords are: - string - number - bool The type constructors allow you to specify complex types such as collections: - list(<TYPE>) - set(<TYPE>) - map(<TYPE>) - object({<ATTR NAME> = <TYPE>, ... }) - tuple([<TYPE>, ...]) The keyword any may be used to indicate that any type is acceptable. For more information on the meaning and behavior of these different types, as well as detailed information about automatic conversion of complex types, see {@link https://www.terraform.io/docs/configuration/types.html|Type Constraints}. If both the type and default arguments are specified, the given default value must be convertible to the specified type.
        :param validation: (experimental) Specify arbitrary custom validation rules for a particular variable using a validation block nested within the corresponding variable block.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformVariable.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TerraformVariableConfig(
            default=default,
            description=description,
            nullable=nullable,
            sensitive=sensitive,
            type=type,
            validation=validation,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="addValidation")
    def add_validation(
        self,
        *,
        condition: typing.Any,
        error_message: builtins.str,
    ) -> None:
        '''
        :param condition: 
        :param error_message: 

        :stability: experimental
        '''
        validation = TerraformVariableValidationConfig(
            condition=condition, error_message=error_message
        )

        return typing.cast(None, jsii.invoke(self, "addValidation", [validation]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="booleanValue")
    def boolean_value(self) -> IResolvable:
        '''
        :stability: experimental
        '''
        return typing.cast(IResolvable, jsii.get(self, "booleanValue"))

    @builtins.property
    @jsii.member(jsii_name="listValue")
    def list_value(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "listValue"))

    @builtins.property
    @jsii.member(jsii_name="numberValue")
    def number_value(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "numberValue"))

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "nullable"))

    @builtins.property
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "sensitive"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="validation")
    def validation(
        self,
    ) -> typing.Optional[typing.List["TerraformVariableValidationConfig"]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List["TerraformVariableValidationConfig"]], jsii.get(self, "validation"))


@jsii.data_type(
    jsii_type="cdktf.TerraformVariableConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default": "default",
        "description": "description",
        "nullable": "nullable",
        "sensitive": "sensitive",
        "type": "type",
        "validation": "validation",
    },
)
class TerraformVariableConfig:
    def __init__(
        self,
        *,
        default: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[builtins.bool] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
        validation: typing.Optional[typing.Sequence[typing.Union["TerraformVariableValidationConfig", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param default: 
        :param description: 
        :param nullable: 
        :param sensitive: 
        :param type: (experimental) The type argument in a variable block allows you to restrict the type of value that will be accepted as the value for a variable. If no type constraint is set then a value of any type is accepted. While type constraints are optional, we recommend specifying them; they serve as easy reminders for users of the module, and allow Terraform to return a helpful error message if the wrong type is used. Type constraints are created from a mixture of type keywords and type constructors. The supported type keywords are: - string - number - bool The type constructors allow you to specify complex types such as collections: - list(<TYPE>) - set(<TYPE>) - map(<TYPE>) - object({<ATTR NAME> = <TYPE>, ... }) - tuple([<TYPE>, ...]) The keyword any may be used to indicate that any type is acceptable. For more information on the meaning and behavior of these different types, as well as detailed information about automatic conversion of complex types, see {@link https://www.terraform.io/docs/configuration/types.html|Type Constraints}. If both the type and default arguments are specified, the given default value must be convertible to the specified type.
        :param validation: (experimental) Specify arbitrary custom validation rules for a particular variable using a validation block nested within the corresponding variable block.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformVariableConfig.__init__)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument nullable", value=nullable, expected_type=type_hints["nullable"])
            check_type(argname="argument sensitive", value=sensitive, expected_type=type_hints["sensitive"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
        self._values: typing.Dict[str, typing.Any] = {}
        if default is not None:
            self._values["default"] = default
        if description is not None:
            self._values["description"] = description
        if nullable is not None:
            self._values["nullable"] = nullable
        if sensitive is not None:
            self._values["sensitive"] = sensitive
        if type is not None:
            self._values["type"] = type
        if validation is not None:
            self._values["validation"] = validation

    @builtins.property
    def default(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        result = self._values.get("default")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nullable(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("nullable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sensitive(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("sensitive")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type argument in a variable block allows you to restrict the type of value that will be accepted as the value for a variable.

        If no type constraint is set then a value of any type is accepted.

        While type constraints are optional, we recommend specifying them; they serve as easy reminders for users of the module, and allow Terraform to return a helpful error message if the wrong type is used.

        Type constraints are created from a mixture of type keywords and type constructors. The supported type keywords are:

        - string
        - number
        - bool

        The type constructors allow you to specify complex types such as collections:

        - list()
        - set()
        - map()
        - object({ = , ... })
        - tuple([, ...])

        The keyword any may be used to indicate that any type is acceptable. For more information on the meaning and behavior of these different types, as well as detailed information about automatic conversion of complex types, see {@link https://www.terraform.io/docs/configuration/types.html|Type Constraints}.

        If both the type and default arguments are specified, the given default value must be convertible to the specified type.

        :stability: experimental
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validation(
        self,
    ) -> typing.Optional[typing.List["TerraformVariableValidationConfig"]]:
        '''(experimental) Specify arbitrary custom validation rules for a particular variable using a validation block nested within the corresponding variable block.

        :stability: experimental
        '''
        result = self._values.get("validation")
        return typing.cast(typing.Optional[typing.List["TerraformVariableValidationConfig"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformVariableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.TerraformVariableValidationConfig",
    jsii_struct_bases=[],
    name_mapping={"condition": "condition", "error_message": "errorMessage"},
)
class TerraformVariableValidationConfig:
    def __init__(self, *, condition: typing.Any, error_message: builtins.str) -> None:
        '''
        :param condition: 
        :param error_message: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformVariableValidationConfig.__init__)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
        self._values: typing.Dict[str, typing.Any] = {
            "condition": condition,
            "error_message": error_message,
        }

    @builtins.property
    def condition(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def error_message(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("error_message")
        assert result is not None, "Required property 'error_message' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformVariableValidationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Testing(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Testing"):
    '''(experimental) Testing utilities for cdktf applications.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="app")
    @builtins.classmethod
    def app(
        cls,
        *,
        enable_future_flags: typing.Optional[builtins.bool] = None,
        fake_cdktf_json_path: typing.Optional[builtins.bool] = None,
        outdir: typing.Optional[builtins.str] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        stub_version: typing.Optional[builtins.bool] = None,
    ) -> App:
        '''(experimental) Returns an app for testing with the following properties: - Output directory is a temp dir.

        :param enable_future_flags: 
        :param fake_cdktf_json_path: 
        :param outdir: 
        :param stack_traces: 
        :param stub_version: 

        :stability: experimental
        '''
        options = TestingAppOptions(
            enable_future_flags=enable_future_flags,
            fake_cdktf_json_path=fake_cdktf_json_path,
            outdir=outdir,
            stack_traces=stack_traces,
            stub_version=stub_version,
        )

        return typing.cast(App, jsii.sinvoke(cls, "app", [options]))

    @jsii.member(jsii_name="enableFutureFlags")
    @builtins.classmethod
    def enable_future_flags(cls, app: App) -> App:
        '''
        :param app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.enable_future_flags)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast(App, jsii.sinvoke(cls, "enableFutureFlags", [app]))

    @jsii.member(jsii_name="fakeCdktfJsonPath")
    @builtins.classmethod
    def fake_cdktf_json_path(cls, app: App) -> App:
        '''
        :param app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.fake_cdktf_json_path)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast(App, jsii.sinvoke(cls, "fakeCdktfJsonPath", [app]))

    @jsii.member(jsii_name="fullSynth")
    @builtins.classmethod
    def full_synth(cls, stack: TerraformStack) -> builtins.str:
        '''
        :param stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.full_synth)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fullSynth", [stack]))

    @jsii.member(jsii_name="renderConstructTree")
    @builtins.classmethod
    def render_construct_tree(cls, construct: constructs.IConstruct) -> builtins.str:
        '''
        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.render_construct_tree)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "renderConstructTree", [construct]))

    @jsii.member(jsii_name="setupJest")
    @builtins.classmethod
    def setup_jest(cls) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.sinvoke(cls, "setupJest", []))

    @jsii.member(jsii_name="stubVersion")
    @builtins.classmethod
    def stub_version(cls, app: App) -> App:
        '''
        :param app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.stub_version)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast(App, jsii.sinvoke(cls, "stubVersion", [app]))

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(
        cls,
        stack: TerraformStack,
        run_validations: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''(experimental) Returns the Terraform synthesized JSON.

        :param stack: -
        :param run_validations: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.synth)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument run_validations", value=run_validations, expected_type=type_hints["run_validations"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "synth", [stack, run_validations]))

    @jsii.member(jsii_name="synthScope")
    @builtins.classmethod
    def synth_scope(cls, fn: IScopeCallback) -> builtins.str:
        '''
        :param fn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.synth_scope)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "synthScope", [fn]))

    @jsii.member(jsii_name="toBeValidTerraform")
    @builtins.classmethod
    def to_be_valid_terraform(cls, received: builtins.str) -> builtins.bool:
        '''
        :param received: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.to_be_valid_terraform)
            check_type(argname="argument received", value=received, expected_type=type_hints["received"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "toBeValidTerraform", [received]))

    @jsii.member(jsii_name="toHaveDataSource")
    @builtins.classmethod
    def to_have_data_source(
        cls,
        received: builtins.str,
        resource_type: builtins.str,
    ) -> builtins.bool:
        '''
        :param received: -
        :param resource_type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.to_have_data_source)
            check_type(argname="argument received", value=received, expected_type=type_hints["received"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "toHaveDataSource", [received, resource_type]))

    @jsii.member(jsii_name="toHaveDataSourceWithProperties")
    @builtins.classmethod
    def to_have_data_source_with_properties(
        cls,
        received: builtins.str,
        resource_type: builtins.str,
        properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> builtins.bool:
        '''
        :param received: -
        :param resource_type: -
        :param properties: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.to_have_data_source_with_properties)
            check_type(argname="argument received", value=received, expected_type=type_hints["received"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "toHaveDataSourceWithProperties", [received, resource_type, properties]))

    @jsii.member(jsii_name="toHaveResource")
    @builtins.classmethod
    def to_have_resource(
        cls,
        received: builtins.str,
        resource_type: builtins.str,
    ) -> builtins.bool:
        '''
        :param received: -
        :param resource_type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.to_have_resource)
            check_type(argname="argument received", value=received, expected_type=type_hints["received"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "toHaveResource", [received, resource_type]))

    @jsii.member(jsii_name="toHaveResourceWithProperties")
    @builtins.classmethod
    def to_have_resource_with_properties(
        cls,
        received: builtins.str,
        resource_type: builtins.str,
        properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> builtins.bool:
        '''
        :param received: -
        :param resource_type: -
        :param properties: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Testing.to_have_resource_with_properties)
            check_type(argname="argument received", value=received, expected_type=type_hints["received"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "toHaveResourceWithProperties", [received, resource_type, properties]))


@jsii.data_type(
    jsii_type="cdktf.TestingAppOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enable_future_flags": "enableFutureFlags",
        "fake_cdktf_json_path": "fakeCdktfJsonPath",
        "outdir": "outdir",
        "stack_traces": "stackTraces",
        "stub_version": "stubVersion",
    },
)
class TestingAppOptions:
    def __init__(
        self,
        *,
        enable_future_flags: typing.Optional[builtins.bool] = None,
        fake_cdktf_json_path: typing.Optional[builtins.bool] = None,
        outdir: typing.Optional[builtins.str] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
        stub_version: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param enable_future_flags: 
        :param fake_cdktf_json_path: 
        :param outdir: 
        :param stack_traces: 
        :param stub_version: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TestingAppOptions.__init__)
            check_type(argname="argument enable_future_flags", value=enable_future_flags, expected_type=type_hints["enable_future_flags"])
            check_type(argname="argument fake_cdktf_json_path", value=fake_cdktf_json_path, expected_type=type_hints["fake_cdktf_json_path"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument stack_traces", value=stack_traces, expected_type=type_hints["stack_traces"])
            check_type(argname="argument stub_version", value=stub_version, expected_type=type_hints["stub_version"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enable_future_flags is not None:
            self._values["enable_future_flags"] = enable_future_flags
        if fake_cdktf_json_path is not None:
            self._values["fake_cdktf_json_path"] = fake_cdktf_json_path
        if outdir is not None:
            self._values["outdir"] = outdir
        if stack_traces is not None:
            self._values["stack_traces"] = stack_traces
        if stub_version is not None:
            self._values["stub_version"] = stub_version

    @builtins.property
    def enable_future_flags(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enable_future_flags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fake_cdktf_json_path(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("fake_cdktf_json_path")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_traces(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stack_traces")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stub_version(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stub_version")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TestingAppOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Token(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Token"):
    '''(experimental) Represents a special or lazily-evaluated value.

    Can be used to delay evaluation of a certain value in case, for example,
    that it requires some context or late-bound data. Can also be used to
    mark values that need special processing at document rendering time.

    Tokens can be embedded into strings while retaining their original
    semantics.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="asAny")
    @builtins.classmethod
    def as_any(cls, value: typing.Any) -> IResolvable:
        '''(experimental) Return a resolvable representation of the given value.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_any)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(IResolvable, jsii.sinvoke(cls, "asAny", [value]))

    @jsii.member(jsii_name="asAnyMap")
    @builtins.classmethod
    def as_any_map(
        cls,
        value: typing.Any,
        *,
        display_hint: typing.Optional[builtins.str] = None,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Return a reversible map representation of this token.

        :param value: -
        :param display_hint: (experimental) A hint for the Token's purpose when stringifying it. Default: - no display hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_any_map)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        options = EncodingOptions(display_hint=display_hint)

        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.sinvoke(cls, "asAnyMap", [value, options]))

    @jsii.member(jsii_name="asBooleanMap")
    @builtins.classmethod
    def as_boolean_map(
        cls,
        value: typing.Any,
        *,
        display_hint: typing.Optional[builtins.str] = None,
    ) -> typing.Mapping[builtins.str, builtins.bool]:
        '''(experimental) Return a reversible map representation of this token.

        :param value: -
        :param display_hint: (experimental) A hint for the Token's purpose when stringifying it. Default: - no display hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_boolean_map)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        options = EncodingOptions(display_hint=display_hint)

        return typing.cast(typing.Mapping[builtins.str, builtins.bool], jsii.sinvoke(cls, "asBooleanMap", [value, options]))

    @jsii.member(jsii_name="asList")
    @builtins.classmethod
    def as_list(
        cls,
        value: typing.Any,
        *,
        display_hint: typing.Optional[builtins.str] = None,
    ) -> typing.List[builtins.str]:
        '''(experimental) Return a reversible list representation of this token.

        :param value: -
        :param display_hint: (experimental) A hint for the Token's purpose when stringifying it. Default: - no display hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_list)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        options = EncodingOptions(display_hint=display_hint)

        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "asList", [value, options]))

    @jsii.member(jsii_name="asMap")
    @builtins.classmethod
    def as_map(
        cls,
        value: typing.Any,
        map_value: typing.Any,
        *,
        display_hint: typing.Optional[builtins.str] = None,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Return a reversible map representation of this token.

        :param value: -
        :param map_value: -
        :param display_hint: (experimental) A hint for the Token's purpose when stringifying it. Default: - no display hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_map)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument map_value", value=map_value, expected_type=type_hints["map_value"])
        options = EncodingOptions(display_hint=display_hint)

        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.sinvoke(cls, "asMap", [value, map_value, options]))

    @jsii.member(jsii_name="asNumber")
    @builtins.classmethod
    def as_number(cls, value: typing.Any) -> jsii.Number:
        '''(experimental) Return a reversible number representation of this token.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_number)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "asNumber", [value]))

    @jsii.member(jsii_name="asNumberList")
    @builtins.classmethod
    def as_number_list(cls, value: typing.Any) -> typing.List[jsii.Number]:
        '''(experimental) Return a reversible list representation of this token.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_number_list)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.List[jsii.Number], jsii.sinvoke(cls, "asNumberList", [value]))

    @jsii.member(jsii_name="asNumberMap")
    @builtins.classmethod
    def as_number_map(
        cls,
        value: typing.Any,
        *,
        display_hint: typing.Optional[builtins.str] = None,
    ) -> typing.Mapping[builtins.str, jsii.Number]:
        '''(experimental) Return a reversible map representation of this token.

        :param value: -
        :param display_hint: (experimental) A hint for the Token's purpose when stringifying it. Default: - no display hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_number_map)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        options = EncodingOptions(display_hint=display_hint)

        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.sinvoke(cls, "asNumberMap", [value, options]))

    @jsii.member(jsii_name="asString")
    @builtins.classmethod
    def as_string(
        cls,
        value: typing.Any,
        *,
        display_hint: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Return a reversible string representation of this token.

        If the Token is initialized with a literal, the stringified value of the
        literal is returned. Otherwise, a special quoted string representation
        of the Token is returned that can be embedded into other strings.

        Strings with quoted Tokens in them can be restored back into
        complex values with the Tokens restored by calling ``resolve()``
        on the string.

        :param value: -
        :param display_hint: (experimental) A hint for the Token's purpose when stringifying it. Default: - no display hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_string)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        options = EncodingOptions(display_hint=display_hint)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "asString", [value, options]))

    @jsii.member(jsii_name="asStringMap")
    @builtins.classmethod
    def as_string_map(
        cls,
        value: typing.Any,
        *,
        display_hint: typing.Optional[builtins.str] = None,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Return a reversible map representation of this token.

        :param value: -
        :param display_hint: (experimental) A hint for the Token's purpose when stringifying it. Default: - no display hint

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.as_string_map)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        options = EncodingOptions(display_hint=display_hint)

        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.sinvoke(cls, "asStringMap", [value, options]))

    @jsii.member(jsii_name="isUnresolved")
    @builtins.classmethod
    def is_unresolved(cls, obj: typing.Any) -> builtins.bool:
        '''(experimental) Returns true if obj represents an unresolved value.

        One of these must be true:

        - ``obj`` is an IResolvable
        - ``obj`` is a string containing at least one encoded ``IResolvable``
        - ``obj`` is either an encoded number or list

        This does NOT recurse into lists or objects to see if they
        containing resolvables.

        :param obj: The object to test.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Token.is_unresolved)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isUnresolved", [obj]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANY_MAP_TOKEN_VALUE")
    def ANY_MAP_TOKEN_VALUE(cls) -> builtins.str:
        '''(experimental) Any map token representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ANY_MAP_TOKEN_VALUE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NUMBER_MAP_TOKEN_VALUE")
    def NUMBER_MAP_TOKEN_VALUE(cls) -> jsii.Number:
        '''(experimental) Number Map token value representation.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "NUMBER_MAP_TOKEN_VALUE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STRING_MAP_TOKEN_VALUE")
    def STRING_MAP_TOKEN_VALUE(cls) -> builtins.str:
        '''(experimental) String Map token value representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "STRING_MAP_TOKEN_VALUE"))


class Tokenization(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Tokenization"):
    '''(experimental) Less oft-needed functions to manipulate Tokens.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="isResolvable")
    @builtins.classmethod
    def is_resolvable(cls, obj: typing.Any) -> builtins.bool:
        '''(experimental) Return whether the given object is an IResolvable object.

        This is different from Token.isUnresolved() which will also check for
        encoded Tokens, whereas this method will only do a type check on the given
        object.

        :param obj: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.is_resolvable)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isResolvable", [obj]))

    @jsii.member(jsii_name="resolve")
    @builtins.classmethod
    def resolve(
        cls,
        obj: typing.Any,
        *,
        resolver: ITokenResolver,
        scope: constructs.IConstruct,
        preparing: typing.Optional[builtins.bool] = None,
    ) -> typing.Any:
        '''(experimental) Resolves an object by evaluating all tokens and removing any undefined or empty objects or arrays.

        Values can only be primitives, arrays or tokens. Other objects (i.e. with methods) will be rejected.

        :param obj: The object to resolve.
        :param resolver: (experimental) The resolver to apply to any resolvable tokens found.
        :param scope: (experimental) The scope from which resolution is performed.
        :param preparing: (experimental) Whether the resolution is being executed during the prepare phase or not. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.resolve)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        options = ResolveOptions(resolver=resolver, scope=scope, preparing=preparing)

        return typing.cast(typing.Any, jsii.sinvoke(cls, "resolve", [obj, options]))

    @jsii.member(jsii_name="reverse")
    @builtins.classmethod
    def reverse(cls, x: typing.Any) -> typing.List[IResolvable]:
        '''(experimental) Reverse any value into Resolvables, if possible.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.reverse)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(typing.List[IResolvable], jsii.sinvoke(cls, "reverse", [x]))

    @jsii.member(jsii_name="reverseList")
    @builtins.classmethod
    def reverse_list(
        cls,
        l: typing.Sequence[builtins.str],
    ) -> typing.Optional[IResolvable]:
        '''(experimental) Un-encode a Tokenized value from a list.

        :param l: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.reverse_list)
            check_type(argname="argument l", value=l, expected_type=type_hints["l"])
        return typing.cast(typing.Optional[IResolvable], jsii.sinvoke(cls, "reverseList", [l]))

    @jsii.member(jsii_name="reverseMap")
    @builtins.classmethod
    def reverse_map(
        cls,
        m: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Optional[IResolvable]:
        '''(experimental) Un-encode a Tokenized value from a map.

        :param m: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.reverse_map)
            check_type(argname="argument m", value=m, expected_type=type_hints["m"])
        return typing.cast(typing.Optional[IResolvable], jsii.sinvoke(cls, "reverseMap", [m]))

    @jsii.member(jsii_name="reverseNumber")
    @builtins.classmethod
    def reverse_number(cls, n: jsii.Number) -> typing.Optional[IResolvable]:
        '''(experimental) Un-encode a Tokenized value from a number.

        :param n: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.reverse_number)
            check_type(argname="argument n", value=n, expected_type=type_hints["n"])
        return typing.cast(typing.Optional[IResolvable], jsii.sinvoke(cls, "reverseNumber", [n]))

    @jsii.member(jsii_name="reverseNumberList")
    @builtins.classmethod
    def reverse_number_list(
        cls,
        l: typing.Sequence[jsii.Number],
    ) -> typing.Optional[IResolvable]:
        '''(experimental) Un-encode a Tokenized value from a list.

        :param l: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.reverse_number_list)
            check_type(argname="argument l", value=l, expected_type=type_hints["l"])
        return typing.cast(typing.Optional[IResolvable], jsii.sinvoke(cls, "reverseNumberList", [l]))

    @jsii.member(jsii_name="reverseString")
    @builtins.classmethod
    def reverse_string(cls, s: builtins.str) -> "TokenizedStringFragments":
        '''(experimental) Un-encode a string potentially containing encoded tokens.

        :param s: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.reverse_string)
            check_type(argname="argument s", value=s, expected_type=type_hints["s"])
        return typing.cast("TokenizedStringFragments", jsii.sinvoke(cls, "reverseString", [s]))

    @jsii.member(jsii_name="stringifyNumber")
    @builtins.classmethod
    def stringify_number(cls, x: jsii.Number) -> builtins.str:
        '''(experimental) Stringify a number directly or lazily if it's a Token.

        If it is an object (i.e., { Ref: 'SomeLogicalId' }), return it as-is.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Tokenization.stringify_number)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "stringifyNumber", [x]))


class TokenizedStringFragments(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TokenizedStringFragments",
):
    '''(experimental) Fragments of a concatenated string containing stringified Tokens.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addIntrinsic")
    def add_intrinsic(self, value: typing.Any) -> None:
        '''(experimental) Adds an intrinsic fragment.

        :param value: the intrinsic value to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TokenizedStringFragments.add_intrinsic)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addIntrinsic", [value]))

    @jsii.member(jsii_name="addLiteral")
    def add_literal(self, lit: typing.Any) -> None:
        '''(experimental) Adds a literal fragment.

        :param lit: the literal to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TokenizedStringFragments.add_literal)
            check_type(argname="argument lit", value=lit, expected_type=type_hints["lit"])
        return typing.cast(None, jsii.invoke(self, "addLiteral", [lit]))

    @jsii.member(jsii_name="addToken")
    def add_token(self, token: IResolvable) -> None:
        '''(experimental) Adds a token fragment.

        :param token: the token to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TokenizedStringFragments.add_token)
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        return typing.cast(None, jsii.invoke(self, "addToken", [token]))

    @jsii.member(jsii_name="join")
    def join(self, concat: IFragmentConcatenator) -> typing.Any:
        '''(experimental) Combine the string fragments using the given joiner.

        If there are any

        :param concat: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TokenizedStringFragments.join)
            check_type(argname="argument concat", value=concat, expected_type=type_hints["concat"])
        return typing.cast(typing.Any, jsii.invoke(self, "join", [concat]))

    @jsii.member(jsii_name="mapTokens")
    def map_tokens(self, mapper: ITokenMapper) -> "TokenizedStringFragments":
        '''(experimental) Apply a transformation function to all tokens in the string.

        :param mapper: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TokenizedStringFragments.map_tokens)
            check_type(argname="argument mapper", value=mapper, expected_type=type_hints["mapper"])
        return typing.cast("TokenizedStringFragments", jsii.invoke(self, "mapTokens", [mapper]))

    @builtins.property
    @jsii.member(jsii_name="firstValue")
    def first_value(self) -> typing.Any:
        '''(experimental) Returns the first value.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "firstValue"))

    @builtins.property
    @jsii.member(jsii_name="intrinsic")
    def intrinsic(self) -> typing.List[IResolvable]:
        '''(experimental) Return all intrinsic fragments from this string.

        :stability: experimental
        '''
        return typing.cast(typing.List[IResolvable], jsii.get(self, "intrinsic"))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        '''(experimental) Returns the number of fragments.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="literals")
    def literals(self) -> typing.List[IResolvable]:
        '''(experimental) Return all literals from this string.

        :stability: experimental
        '''
        return typing.cast(typing.List[IResolvable], jsii.get(self, "literals"))

    @builtins.property
    @jsii.member(jsii_name="tokens")
    def tokens(self) -> typing.List[IResolvable]:
        '''(experimental) Return all Tokens from this string.

        :stability: experimental
        '''
        return typing.cast(typing.List[IResolvable], jsii.get(self, "tokens"))

    @builtins.property
    @jsii.member(jsii_name="firstToken")
    def first_token(self) -> typing.Optional[IResolvable]:
        '''(experimental) Returns the first token.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IResolvable], jsii.get(self, "firstToken"))


class VariableType(metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.VariableType"):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="list")
    @builtins.classmethod
    def list(cls, type: builtins.str) -> builtins.str:
        '''
        :param type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VariableType.list)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "list", [type]))

    @jsii.member(jsii_name="map")
    @builtins.classmethod
    def map(cls, type: builtins.str) -> builtins.str:
        '''
        :param type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VariableType.map)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "map", [type]))

    @jsii.member(jsii_name="object")
    @builtins.classmethod
    def object(
        cls,
        attributes: typing.Mapping[builtins.str, builtins.str],
    ) -> builtins.str:
        '''
        :param attributes: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VariableType.object)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "object", [attributes]))

    @jsii.member(jsii_name="set")
    @builtins.classmethod
    def set(cls, type: builtins.str) -> builtins.str:
        '''
        :param type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VariableType.set)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "set", [type]))

    @jsii.member(jsii_name="tuple")
    @builtins.classmethod
    def tuple(cls, *elements: builtins.str) -> builtins.str:
        '''
        :param elements: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(VariableType.tuple)
            check_type(argname="argument elements", value=elements, expected_type=typing.Tuple[type_hints["elements"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(builtins.str, jsii.sinvoke(cls, "tuple", [*elements]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANY")
    def ANY(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ANY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BOOL")
    def BOOL(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "BOOL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LIST")
    def LIST(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LIST"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LIST_BOOL")
    def LIST_BOOL(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LIST_BOOL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LIST_NUMBER")
    def LIST_NUMBER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LIST_NUMBER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LIST_STRING")
    def LIST_STRING(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LIST_STRING"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAP")
    def MAP(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MAP"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAP_BOOL")
    def MAP_BOOL(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MAP_BOOL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAP_NUMBER")
    def MAP_NUMBER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MAP_NUMBER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAP_STRING")
    def MAP_STRING(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MAP_STRING"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NUMBER")
    def NUMBER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "NUMBER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SET")
    def SET(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "SET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SET_BOOL")
    def SET_BOOL(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "SET_BOOL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SET_NUMBER")
    def SET_NUMBER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "SET_NUMBER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SET_STRING")
    def SET_STRING(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "SET_STRING"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STRING")
    def STRING(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "STRING"))


class _VariableTypeProxy(VariableType):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, VariableType).__jsii_proxy_class__ = lambda : _VariableTypeProxy


@jsii.data_type(
    jsii_type="cdktf.WinrmProvisionerConnection",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "type": "type",
        "cacert": "cacert",
        "https": "https",
        "insecure": "insecure",
        "password": "password",
        "port": "port",
        "script_path": "scriptPath",
        "timeout": "timeout",
        "use_ntlm": "useNtlm",
        "user": "user",
    },
)
class WinrmProvisionerConnection:
    def __init__(
        self,
        *,
        host: builtins.str,
        type: builtins.str,
        cacert: typing.Optional[builtins.str] = None,
        https: typing.Optional[builtins.bool] = None,
        insecure: typing.Optional[builtins.bool] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        script_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
        use_ntlm: typing.Optional[builtins.bool] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Most provisioners require access to the remote resource via SSH or WinRM and expect a nested connection block with details about how to connect.

        See {@link https://www.terraform.io/language/resources/provisioners/connection connection}

        :param host: (experimental) The address of the resource to connect to.
        :param type: (experimental) The connection type. Valid values are "ssh" and "winrm". Provisioners typically assume that the remote system runs Microsoft Windows when using WinRM. Behaviors based on the SSH target_platform will force Windows-specific behavior for WinRM, unless otherwise specified.
        :param cacert: (experimental) The CA certificate to validate against.
        :param https: (experimental) Set to true to connect using HTTPS instead of HTTP.
        :param insecure: (experimental) Set to true to skip validating the HTTPS certificate chain.
        :param password: (experimental) The password to use for the connection.
        :param port: (experimental) The port to connect to. Default: 22
        :param script_path: (experimental) The path used to copy scripts meant for remote execution. Refer to {@link https://www.terraform.io/language/resources/provisioners/connection#how-provisioners-execute-remote-scripts How Provisioners Execute Remote Scripts below for more details}
        :param timeout: (experimental) The timeout to wait for the connection to become available. Should be provided as a string (e.g., "30s" or "5m".) Default: 5m
        :param use_ntlm: (experimental) Set to true to use NTLM authentication rather than default (basic authentication), removing the requirement for basic authentication to be enabled within the target guest. Refer to Authentication for Remote Connections in the Windows App Development documentation for more details.
        :param user: (experimental) The user to use for the connection. Default: root

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WinrmProvisionerConnection.__init__)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument cacert", value=cacert, expected_type=type_hints["cacert"])
            check_type(argname="argument https", value=https, expected_type=type_hints["https"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument script_path", value=script_path, expected_type=type_hints["script_path"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument use_ntlm", value=use_ntlm, expected_type=type_hints["use_ntlm"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[str, typing.Any] = {
            "host": host,
            "type": type,
        }
        if cacert is not None:
            self._values["cacert"] = cacert
        if https is not None:
            self._values["https"] = https
        if insecure is not None:
            self._values["insecure"] = insecure
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if script_path is not None:
            self._values["script_path"] = script_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if use_ntlm is not None:
            self._values["use_ntlm"] = use_ntlm
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def host(self) -> builtins.str:
        '''(experimental) The address of the resource to connect to.

        :stability: experimental
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) The connection type.

        Valid values are "ssh" and "winrm".
        Provisioners typically assume that the remote system runs Microsoft Windows when using WinRM.
        Behaviors based on the SSH target_platform will force Windows-specific behavior for WinRM, unless otherwise specified.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cacert(self) -> typing.Optional[builtins.str]:
        '''(experimental) The CA certificate to validate against.

        :stability: experimental
        '''
        result = self._values.get("cacert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to connect using HTTPS instead of HTTP.

        :stability: experimental
        '''
        result = self._values.get("https")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def insecure(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to skip validating the HTTPS certificate chain.

        :stability: experimental
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) The password to use for the connection.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port to connect to.

        :default: 22

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def script_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path used to copy scripts meant for remote execution.

        Refer to {@link https://www.terraform.io/language/resources/provisioners/connection#how-provisioners-execute-remote-scripts How Provisioners Execute Remote Scripts below for more details}

        :stability: experimental
        '''
        result = self._values.get("script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''(experimental) The timeout to wait for the connection to become available.

        Should be provided as a string (e.g., "30s" or "5m".)

        :default: 5m

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ntlm(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to use NTLM authentication rather than default (basic authentication), removing the requirement for basic authentication to be enabled within the target guest.

        Refer to Authentication for Remote Connections in the Windows App Development documentation for more details.

        :stability: experimental
        '''
        result = self._values.get("use_ntlm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user to use for the connection.

        :default: root

        :stability: experimental
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WinrmProvisionerConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITerraformAddressable, IResolvable)
class AnyMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.AnyMap"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AnyMap.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: builtins.str) -> typing.Any:
        '''
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AnyMap.lookup)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Any, jsii.invoke(self, "lookup", [key]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AnyMap.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(AnyMap, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(AnyMap, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)


@jsii.implements(ITerraformAddressable, IInterpolatingParent, IResolvable)
class AnyMapList(metaclass=jsii.JSIIMeta, jsii_type="cdktf.AnyMapList"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -
        :param wraps_set: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AnyMapList.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> AnyMap:
        '''
        :param index: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AnyMapList.get)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast(AnyMap, jsii.invoke(self, "get", [index]))

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, property: builtins.str) -> IResolvable:
        '''
        :param property: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AnyMapList.interpolation_for_attribute)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [property]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AnyMapList.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(AnyMapList, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(AnyMapList, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(AnyMapList, "_wraps_set").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.implements(ITerraformAddressable, IResolvable)
class BooleanMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.BooleanMap"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BooleanMap.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: builtins.str) -> IResolvable:
        '''
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BooleanMap.lookup)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(IResolvable, jsii.invoke(self, "lookup", [key]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BooleanMap.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(BooleanMap, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(BooleanMap, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)


@jsii.implements(ITerraformAddressable, IInterpolatingParent, IResolvable)
class BooleanMapList(metaclass=jsii.JSIIMeta, jsii_type="cdktf.BooleanMapList"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -
        :param wraps_set: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BooleanMapList.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> BooleanMap:
        '''
        :param index: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BooleanMapList.get)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast(BooleanMap, jsii.invoke(self, "get", [index]))

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, property: builtins.str) -> IResolvable:
        '''
        :param property: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BooleanMapList.interpolation_for_attribute)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [property]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BooleanMapList.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(BooleanMapList, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(BooleanMapList, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(BooleanMapList, "_wraps_set").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.implements(IInterpolatingParent, IResolvable, ITerraformAddressable)
class ComplexComputedList(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.ComplexComputedList",
):
    '''
    :deprecated:

    Going to be replaced by Array of ComplexListItem
    and will be removed in the future

    :stability: deprecated
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_computed_list_index: builtins.str,
        wraps_set: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -
        :param complex_computed_list_index: -
        :param wraps_set: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_computed_list_index", value=complex_computed_list_index, expected_type=type_hints["complex_computed_list_index"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_computed_list_index, wraps_set])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="getAnyMapAttribute")
    def get_any_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_any_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "getAnyMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: builtins.str) -> IResolvable:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_boolean_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "getBooleanAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getBooleanMapAttribute")
    def get_boolean_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.bool]:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_boolean_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.bool], jsii.invoke(self, "getBooleanMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.List[builtins.str]:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_list_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getListAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: builtins.str) -> jsii.Number:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_number_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getNumberAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberListAttribute")
    def get_number_list_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.List[jsii.Number]:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_number_list_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.List[jsii.Number], jsii.invoke(self, "getNumberListAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberMapAttribute")
    def get_number_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, jsii.Number]:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_number_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.invoke(self, "getNumberMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: builtins.str) -> builtins.str:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_string_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(builtins.str, jsii.invoke(self, "getStringAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getStringMapAttribute")
    def get_string_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :param terraform_attribute: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.get_string_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "getStringMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, property: builtins.str) -> IResolvable:
        '''
        :param property: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.interpolation_for_attribute)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [property]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(deprecated) Produce the Token's value at resolution time.

        :param _context: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexComputedList.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(deprecated) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(deprecated) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: deprecated
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="complexComputedListIndex")
    def _complex_computed_list_index(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "complexComputedListIndex"))

    @_complex_computed_list_index.setter
    def _complex_computed_list_index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexComputedList, "_complex_computed_list_index").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complexComputedListIndex", value)

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexComputedList, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: deprecated
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexComputedList, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: deprecated
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexComputedList, "_wraps_set").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.implements(ITerraformAddressable, IResolvable)
class ComplexList(metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.ComplexList"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -
        :param wraps_set: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexList.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexList.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexList, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexList, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexList, "_wraps_set").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class _ComplexListProxy(ComplexList):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ComplexList).__jsii_proxy_class__ = lambda : _ComplexListProxy


@jsii.implements(ITerraformAddressable, IResolvable)
class ComplexMap(metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.ComplexMap"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexMap.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexMap.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexMap, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexMap, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)


class _ComplexMapProxy(ComplexMap):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ComplexMap).__jsii_proxy_class__ = lambda : _ComplexMapProxy


@jsii.implements(IInterpolatingParent, IResolvable, ITerraformAddressable)
class ComplexObject(metaclass=jsii.JSIIMeta, jsii_type="cdktf.ComplexObject"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_is_from_set: builtins.bool,
        complex_object_index: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
    ) -> None:
        '''
        :param terraform_resource: -
        :param terraform_attribute: -
        :param complex_object_is_from_set: set to true if this item is from inside a set and needs tolist() for accessing it set to "0" for single list items.
        :param complex_object_index: the index of the complex object in a list.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.__init__)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_is_from_set, complex_object_index])

    @jsii.member(jsii_name="computeFqn")
    def compute_fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "computeFqn", []))

    @jsii.member(jsii_name="getAnyMapAttribute")
    def get_any_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_any_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "getAnyMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: builtins.str) -> IResolvable:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_boolean_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "getBooleanAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getBooleanMapAttribute")
    def get_boolean_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.bool]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_boolean_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.bool], jsii.invoke(self, "getBooleanMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.List[builtins.str]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_list_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getListAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: builtins.str) -> jsii.Number:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_number_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getNumberAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberListAttribute")
    def get_number_list_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.List[jsii.Number]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_number_list_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.List[jsii.Number], jsii.invoke(self, "getNumberListAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberMapAttribute")
    def get_number_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, jsii.Number]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_number_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.invoke(self, "getNumberMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: builtins.str) -> builtins.str:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_string_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(builtins.str, jsii.invoke(self, "getStringAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getStringMapAttribute")
    def get_string_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.get_string_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "getStringMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="interpolationAsList")
    def _interpolation_as_list(self) -> IResolvable:
        '''
        :stability: experimental
        '''
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationAsList", []))

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, property: builtins.str) -> IResolvable:
        '''
        :param property: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.interpolation_for_attribute)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [property]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: IResolveContext) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ComplexObject.resolve)
            check_type(argname="argument _context", value=_context, expected_type=type_hints["_context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_context]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fqn"))

    @builtins.property
    @jsii.member(jsii_name="complexObjectIsFromSet")
    def _complex_object_is_from_set(self) -> builtins.bool:
        '''(experimental) set to true if this item is from inside a set and needs tolist() for accessing it set to "0" for single list items.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "complexObjectIsFromSet"))

    @_complex_object_is_from_set.setter
    def _complex_object_is_from_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexObject, "_complex_object_is_from_set").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complexObjectIsFromSet", value)

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexObject, "_terraform_attribute").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> IInterpolatingParent:
        '''
        :stability: experimental
        '''
        return typing.cast(IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexObject, "_terraform_resource").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="complexObjectIndex")
    def _complex_object_index(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number]]:
        '''(experimental) the index of the complex object in a list.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number]], jsii.get(self, "complexObjectIndex"))

    @_complex_object_index.setter
    def _complex_object_index(
        self,
        value: typing.Optional[typing.Union[builtins.str, jsii.Number]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(ComplexObject, "_complex_object_index").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complexObjectIndex", value)


class DataTerraformRemoteState(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteState",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        organization: builtins.str,
        workspaces: IRemoteWorkspace,
        hostname: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteState.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateRemoteConfig(
            defaults=defaults,
            workspace=workspace,
            organization=organization,
            workspaces=workspaces,
            hostname=hostname,
            token=token,
        )

        jsii.create(self.__class__, self, [scope, id, config])


class DataTerraformRemoteStateArtifactory(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateArtifactory",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        password: builtins.str,
        repo: builtins.str,
        subpath: builtins.str,
        url: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param password: (experimental) (Required) - The password.
        :param repo: (experimental) (Required) - The repository name.
        :param subpath: (experimental) (Required) - Path within the repository.
        :param url: (experimental) (Required) - The URL. Note that this is the base url to artifactory not the full repo and subpath.
        :param username: (experimental) (Required) - The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateArtifactory.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateArtifactoryConfig(
            defaults=defaults,
            workspace=workspace,
            password=password,
            repo=repo,
            subpath=subpath,
            url=url,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateArtifactoryConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, ArtifactoryBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "password": "password",
        "repo": "repo",
        "subpath": "subpath",
        "url": "url",
        "username": "username",
    },
)
class DataTerraformRemoteStateArtifactoryConfig(
    DataTerraformRemoteStateConfig,
    ArtifactoryBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        password: builtins.str,
        repo: builtins.str,
        subpath: builtins.str,
        url: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param password: (experimental) (Required) - The password.
        :param repo: (experimental) (Required) - The repository name.
        :param subpath: (experimental) (Required) - Path within the repository.
        :param url: (experimental) (Required) - The URL. Note that this is the base url to artifactory not the full repo and subpath.
        :param username: (experimental) (Required) - The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateArtifactoryConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument repo", value=repo, expected_type=type_hints["repo"])
            check_type(argname="argument subpath", value=subpath, expected_type=type_hints["subpath"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
            "repo": repo,
            "subpath": subpath,
            "url": url,
            "username": username,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> builtins.str:
        '''(experimental) (Required) - The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo(self) -> builtins.str:
        '''(experimental) (Required) - The repository name.

        :stability: experimental
        '''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subpath(self) -> builtins.str:
        '''(experimental) (Required) - Path within the repository.

        :stability: experimental
        '''
        result = self._values.get("subpath")
        assert result is not None, "Required property 'subpath' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) (Required) - The URL.

        Note that this is the base url to artifactory not the full repo and subpath.

        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) (Required) - The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateArtifactoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateAzurerm(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateAzurerm",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        container_name: builtins.str,
        key: builtins.str,
        storage_account_name: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        msi_endpoint: typing.Optional[builtins.str] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        sas_token: typing.Optional[builtins.str] = None,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_msi: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param container_name: (experimental) (Required) The Name of the Storage Container within the Storage Account.
        :param key: (experimental) (Required) The name of the Blob used to retrieve/store Terraform's State file inside the Storage Container.
        :param storage_account_name: (experimental) (Required) The Name of the Storage Account.
        :param access_key: (experimental) access_key - (Optional) The Access Key used to access the Blob Storage Account. This can also be sourced from the ARM_ACCESS_KEY environment variable.
        :param client_id: (experimental) (Optional) The Client ID of the Service Principal. This can also be sourced from the ARM_CLIENT_ID environment variable.
        :param client_secret: (experimental) (Optional) The Client Secret of the Service Principal. This can also be sourced from the ARM_CLIENT_SECRET environment variable.
        :param endpoint: (experimental) (Optional) The Custom Endpoint for Azure Resource Manager. This can also be sourced from the ARM_ENDPOINT environment variable. NOTE: An endpoint should only be configured when using Azure Stack.
        :param environment: (experimental) (Optional) The Azure Environment which should be used. This can also be sourced from the ARM_ENVIRONMENT environment variable. Possible values are public, china, german, stack and usgovernment. Defaults to public.
        :param msi_endpoint: (experimental) (Optional) The path to a custom Managed Service Identity endpoint which is automatically determined if not specified. This can also be sourced from the ARM_MSI_ENDPOINT environment variable.
        :param resource_group_name: (experimental) (Required) The Name of the Resource Group in which the Storage Account exists.
        :param sas_token: (experimental) (Optional) The SAS Token used to access the Blob Storage Account. This can also be sourced from the ARM_SAS_TOKEN environment variable.
        :param subscription_id: (experimental) (Optional) The Subscription ID in which the Storage Account exists. This can also be sourced from the ARM_SUBSCRIPTION_ID environment variable.
        :param tenant_id: (experimental) (Optional) The Tenant ID in which the Subscription exists. This can also be sourced from the ARM_TENANT_ID environment variable.
        :param use_msi: (experimental) (Optional) Should Managed Service Identity authentication be used? This can also be sourced from the ARM_USE_MSI environment variable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateAzurerm.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateAzurermConfig(
            defaults=defaults,
            workspace=workspace,
            container_name=container_name,
            key=key,
            storage_account_name=storage_account_name,
            access_key=access_key,
            client_id=client_id,
            client_secret=client_secret,
            endpoint=endpoint,
            environment=environment,
            msi_endpoint=msi_endpoint,
            resource_group_name=resource_group_name,
            sas_token=sas_token,
            subscription_id=subscription_id,
            tenant_id=tenant_id,
            use_msi=use_msi,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateAzurermConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, AzurermBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "container_name": "containerName",
        "key": "key",
        "storage_account_name": "storageAccountName",
        "access_key": "accessKey",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "endpoint": "endpoint",
        "environment": "environment",
        "msi_endpoint": "msiEndpoint",
        "resource_group_name": "resourceGroupName",
        "sas_token": "sasToken",
        "subscription_id": "subscriptionId",
        "tenant_id": "tenantId",
        "use_msi": "useMsi",
    },
)
class DataTerraformRemoteStateAzurermConfig(
    DataTerraformRemoteStateConfig,
    AzurermBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        container_name: builtins.str,
        key: builtins.str,
        storage_account_name: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        msi_endpoint: typing.Optional[builtins.str] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        sas_token: typing.Optional[builtins.str] = None,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_msi: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param container_name: (experimental) (Required) The Name of the Storage Container within the Storage Account.
        :param key: (experimental) (Required) The name of the Blob used to retrieve/store Terraform's State file inside the Storage Container.
        :param storage_account_name: (experimental) (Required) The Name of the Storage Account.
        :param access_key: (experimental) access_key - (Optional) The Access Key used to access the Blob Storage Account. This can also be sourced from the ARM_ACCESS_KEY environment variable.
        :param client_id: (experimental) (Optional) The Client ID of the Service Principal. This can also be sourced from the ARM_CLIENT_ID environment variable.
        :param client_secret: (experimental) (Optional) The Client Secret of the Service Principal. This can also be sourced from the ARM_CLIENT_SECRET environment variable.
        :param endpoint: (experimental) (Optional) The Custom Endpoint for Azure Resource Manager. This can also be sourced from the ARM_ENDPOINT environment variable. NOTE: An endpoint should only be configured when using Azure Stack.
        :param environment: (experimental) (Optional) The Azure Environment which should be used. This can also be sourced from the ARM_ENVIRONMENT environment variable. Possible values are public, china, german, stack and usgovernment. Defaults to public.
        :param msi_endpoint: (experimental) (Optional) The path to a custom Managed Service Identity endpoint which is automatically determined if not specified. This can also be sourced from the ARM_MSI_ENDPOINT environment variable.
        :param resource_group_name: (experimental) (Required) The Name of the Resource Group in which the Storage Account exists.
        :param sas_token: (experimental) (Optional) The SAS Token used to access the Blob Storage Account. This can also be sourced from the ARM_SAS_TOKEN environment variable.
        :param subscription_id: (experimental) (Optional) The Subscription ID in which the Storage Account exists. This can also be sourced from the ARM_SUBSCRIPTION_ID environment variable.
        :param tenant_id: (experimental) (Optional) The Tenant ID in which the Subscription exists. This can also be sourced from the ARM_TENANT_ID environment variable.
        :param use_msi: (experimental) (Optional) Should Managed Service Identity authentication be used? This can also be sourced from the ARM_USE_MSI environment variable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateAzurermConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument storage_account_name", value=storage_account_name, expected_type=type_hints["storage_account_name"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument msi_endpoint", value=msi_endpoint, expected_type=type_hints["msi_endpoint"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sas_token", value=sas_token, expected_type=type_hints["sas_token"])
            check_type(argname="argument subscription_id", value=subscription_id, expected_type=type_hints["subscription_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument use_msi", value=use_msi, expected_type=type_hints["use_msi"])
        self._values: typing.Dict[str, typing.Any] = {
            "container_name": container_name,
            "key": key,
            "storage_account_name": storage_account_name,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if access_key is not None:
            self._values["access_key"] = access_key
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if environment is not None:
            self._values["environment"] = environment
        if msi_endpoint is not None:
            self._values["msi_endpoint"] = msi_endpoint
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name
        if sas_token is not None:
            self._values["sas_token"] = sas_token
        if subscription_id is not None:
            self._values["subscription_id"] = subscription_id
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if use_msi is not None:
            self._values["use_msi"] = use_msi

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_name(self) -> builtins.str:
        '''(experimental) (Required) The Name of the Storage Container within the Storage Account.

        :stability: experimental
        '''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) (Required) The name of the Blob used to retrieve/store Terraform's State file inside the Storage Container.

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_name(self) -> builtins.str:
        '''(experimental) (Required) The Name of the Storage Account.

        :stability: experimental
        '''
        result = self._values.get("storage_account_name")
        assert result is not None, "Required property 'storage_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) access_key - (Optional) The Access Key used to access the Blob Storage Account.

        This can also be sourced from the ARM_ACCESS_KEY environment variable.

        :stability: experimental
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Client ID of the Service Principal.

        This can also be sourced from the ARM_CLIENT_ID environment variable.

        :stability: experimental
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Client Secret of the Service Principal.

        This can also be sourced from the ARM_CLIENT_SECRET environment variable.

        :stability: experimental
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Custom Endpoint for Azure Resource Manager. This can also be sourced from the ARM_ENDPOINT environment variable.

        NOTE: An endpoint should only be configured when using Azure Stack.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Azure Environment which should be used.

        This can also be sourced from the ARM_ENVIRONMENT environment variable.
        Possible values are public, china, german, stack and usgovernment. Defaults to public.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def msi_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to a custom Managed Service Identity endpoint which is automatically determined if not specified.

        This can also be sourced from the ARM_MSI_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("msi_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Required) The Name of the Resource Group in which the Storage Account exists.

        :stability: experimental
        '''
        result = self._values.get("resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sas_token(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The SAS Token used to access the Blob Storage Account.

        This can also be sourced from the ARM_SAS_TOKEN environment variable.

        :stability: experimental
        '''
        result = self._values.get("sas_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Subscription ID in which the Storage Account exists.

        This can also be sourced from the ARM_SUBSCRIPTION_ID environment variable.

        :stability: experimental
        '''
        result = self._values.get("subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The Tenant ID in which the Subscription exists.

        This can also be sourced from the ARM_TENANT_ID environment variable.

        :stability: experimental
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_msi(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Should Managed Service Identity authentication be used?

        This can also be sourced from the ARM_USE_MSI environment variable.

        :stability: experimental
        '''
        result = self._values.get("use_msi")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateAzurermConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateConsul(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateConsul",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        access_token: builtins.str,
        path: builtins.str,
        address: typing.Optional[builtins.str] = None,
        ca_file: typing.Optional[builtins.str] = None,
        cert_file: typing.Optional[builtins.str] = None,
        datacenter: typing.Optional[builtins.str] = None,
        gzip: typing.Optional[builtins.bool] = None,
        http_auth: typing.Optional[builtins.str] = None,
        key_file: typing.Optional[builtins.str] = None,
        lock: typing.Optional[builtins.bool] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param access_token: (experimental) (Required) Access token.
        :param path: (experimental) (Required) Path in the Consul KV store.
        :param address: (experimental) (Optional) DNS name and port of your Consul endpoint specified in the format dnsname:port. Defaults to the local agent HTTP listener.
        :param ca_file: (experimental) (Optional) A path to a PEM-encoded certificate authority used to verify the remote agent's certificate.
        :param cert_file: (experimental) (Optional) A path to a PEM-encoded certificate provided to the remote agent; requires use of key_file.
        :param datacenter: (experimental) (Optional) The datacenter to use. Defaults to that of the agent.
        :param gzip: (experimental) (Optional) true to compress the state data using gzip, or false (the default) to leave it uncompressed.
        :param http_auth: (experimental) (Optional) HTTP Basic Authentication credentials to be used when communicating with Consul, in the format of either user or user:pass.
        :param key_file: (experimental) (Optional) A path to a PEM-encoded private key, required if cert_file is specified.
        :param lock: (experimental) (Optional) false to disable locking. This defaults to true, but will require session permissions with Consul and at least kv write permissions on $path/.lock to perform locking.
        :param scheme: (experimental) (Optional) Specifies what protocol to use when talking to the given address,either http or https. SSL support can also be triggered by setting then environment variable CONSUL_HTTP_SSL to true.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateConsul.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateConsulConfig(
            defaults=defaults,
            workspace=workspace,
            access_token=access_token,
            path=path,
            address=address,
            ca_file=ca_file,
            cert_file=cert_file,
            datacenter=datacenter,
            gzip=gzip,
            http_auth=http_auth,
            key_file=key_file,
            lock=lock,
            scheme=scheme,
        )

        jsii.create(self.__class__, self, [scope, id, config])


class DataTerraformRemoteStateCos(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateCos",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        bucket: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_id: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param bucket: (experimental) (Required) The name of the COS bucket. You shall manually create it first.
        :param acl: (experimental) (Optional) Object ACL to be applied to the state file, allows private and public-read. Defaults to private.
        :param encrypt: (experimental) (Optional) Whether to enable server side encryption of the state file. If it is true, COS will use 'AES256' encryption algorithm to encrypt state file.
        :param key: (experimental) (Optional) The path for saving the state file in bucket. Defaults to terraform.tfstate.
        :param prefix: (experimental) (Optional) The directory for saving the state file in bucket. Default to "env:".
        :param region: (experimental) (Optional) The region of the COS bucket. It supports environment variables TENCENTCLOUD_REGION.
        :param secret_id: (experimental) (Optional) Secret id of Tencent Cloud. It supports environment variables TENCENTCLOUD_SECRET_ID.
        :param secret_key: (experimental) (Optional) Secret key of Tencent Cloud. It supports environment variables TENCENTCLOUD_SECRET_KEY.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateCos.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateCosConfig(
            defaults=defaults,
            workspace=workspace,
            bucket=bucket,
            acl=acl,
            encrypt=encrypt,
            key=key,
            prefix=prefix,
            region=region,
            secret_id=secret_id,
            secret_key=secret_key,
        )

        jsii.create(self.__class__, self, [scope, id, config])


class DataTerraformRemoteStateEtcd(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateEtcd",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        endpoints: builtins.str,
        path: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param endpoints: (experimental) (Required) A space-separated list of the etcd endpoints.
        :param path: (experimental) (Required) The path where to store the state.
        :param password: (experimental) (Optional) The password.
        :param username: (experimental) (Optional) The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateEtcd.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateEtcdConfig(
            defaults=defaults,
            workspace=workspace,
            endpoints=endpoints,
            path=path,
            password=password,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateEtcdConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, EtcdBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "endpoints": "endpoints",
        "path": "path",
        "password": "password",
        "username": "username",
    },
)
class DataTerraformRemoteStateEtcdConfig(
    DataTerraformRemoteStateConfig,
    EtcdBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        endpoints: builtins.str,
        path: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param endpoints: (experimental) (Required) A space-separated list of the etcd endpoints.
        :param path: (experimental) (Required) The path where to store the state.
        :param password: (experimental) (Optional) The password.
        :param username: (experimental) (Optional) The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateEtcdConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "endpoints": endpoints,
            "path": path,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoints(self) -> builtins.str:
        '''(experimental) (Required) A space-separated list of the etcd endpoints.

        :stability: experimental
        '''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) (Required) The path where to store the state.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateEtcdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateEtcdV3(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateEtcdV3",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        endpoints: typing.Sequence[builtins.str],
        cacert_path: typing.Optional[builtins.str] = None,
        cert_path: typing.Optional[builtins.str] = None,
        key_path: typing.Optional[builtins.str] = None,
        lock: typing.Optional[builtins.bool] = None,
        password: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param endpoints: (experimental) (Required) The list of 'etcd' endpoints which to connect to.
        :param cacert_path: (experimental) (Optional) The path to a PEM-encoded CA bundle with which to verify certificates of TLS-enabled etcd servers.
        :param cert_path: (experimental) (Optional) The path to a PEM-encoded certificate to provide to etcd for secure client identification.
        :param key_path: (experimental) (Optional) The path to a PEM-encoded key to provide to etcd for secure client identification.
        :param lock: (experimental) (Optional) Whether to lock state access. Defaults to true.
        :param password: (experimental) (Optional) Password used to connect to the etcd cluster.
        :param prefix: (experimental) (Optional) An optional prefix to be added to keys when to storing state in etcd. Defaults to "".
        :param username: (experimental) (Optional) Username used to connect to the etcd cluster.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateEtcdV3.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateEtcdV3Config(
            defaults=defaults,
            workspace=workspace,
            endpoints=endpoints,
            cacert_path=cacert_path,
            cert_path=cert_path,
            key_path=key_path,
            lock=lock,
            password=password,
            prefix=prefix,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateEtcdV3Config",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, EtcdV3BackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "endpoints": "endpoints",
        "cacert_path": "cacertPath",
        "cert_path": "certPath",
        "key_path": "keyPath",
        "lock": "lock",
        "password": "password",
        "prefix": "prefix",
        "username": "username",
    },
)
class DataTerraformRemoteStateEtcdV3Config(
    DataTerraformRemoteStateConfig,
    EtcdV3BackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        endpoints: typing.Sequence[builtins.str],
        cacert_path: typing.Optional[builtins.str] = None,
        cert_path: typing.Optional[builtins.str] = None,
        key_path: typing.Optional[builtins.str] = None,
        lock: typing.Optional[builtins.bool] = None,
        password: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param endpoints: (experimental) (Required) The list of 'etcd' endpoints which to connect to.
        :param cacert_path: (experimental) (Optional) The path to a PEM-encoded CA bundle with which to verify certificates of TLS-enabled etcd servers.
        :param cert_path: (experimental) (Optional) The path to a PEM-encoded certificate to provide to etcd for secure client identification.
        :param key_path: (experimental) (Optional) The path to a PEM-encoded key to provide to etcd for secure client identification.
        :param lock: (experimental) (Optional) Whether to lock state access. Defaults to true.
        :param password: (experimental) (Optional) Password used to connect to the etcd cluster.
        :param prefix: (experimental) (Optional) An optional prefix to be added to keys when to storing state in etcd. Defaults to "".
        :param username: (experimental) (Optional) Username used to connect to the etcd cluster.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateEtcdV3Config.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument cacert_path", value=cacert_path, expected_type=type_hints["cacert_path"])
            check_type(argname="argument cert_path", value=cert_path, expected_type=type_hints["cert_path"])
            check_type(argname="argument key_path", value=key_path, expected_type=type_hints["key_path"])
            check_type(argname="argument lock", value=lock, expected_type=type_hints["lock"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "endpoints": endpoints,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if cacert_path is not None:
            self._values["cacert_path"] = cacert_path
        if cert_path is not None:
            self._values["cert_path"] = cert_path
        if key_path is not None:
            self._values["key_path"] = key_path
        if lock is not None:
            self._values["lock"] = lock
        if password is not None:
            self._values["password"] = password
        if prefix is not None:
            self._values["prefix"] = prefix
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoints(self) -> typing.List[builtins.str]:
        '''(experimental) (Required) The list of 'etcd' endpoints which to connect to.

        :stability: experimental
        '''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cacert_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to a PEM-encoded CA bundle with which to verify certificates of TLS-enabled etcd servers.

        :stability: experimental
        '''
        result = self._values.get("cacert_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to a PEM-encoded certificate to provide to etcd for secure client identification.

        :stability: experimental
        '''
        result = self._values.get("cert_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to a PEM-encoded key to provide to etcd for secure client identification.

        :stability: experimental
        '''
        result = self._values.get("key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Whether to lock state access.

        Defaults to true.

        :stability: experimental
        '''
        result = self._values.get("lock")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Password used to connect to the etcd cluster.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) An optional prefix to be added to keys when to storing state in etcd.

        Defaults to "".

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Username used to connect to the etcd cluster.

        :stability: experimental
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateEtcdV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateGcs(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateGcs",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        bucket: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        impersonate_service_account: typing.Optional[builtins.str] = None,
        impersonate_service_account_delegates: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param bucket: (experimental) (Required) The name of the GCS bucket. This name must be globally unique.
        :param access_token: (experimental) (Optional) A temporary [OAuth 2.0 access token] obtained from the Google Authorization server, i.e. the Authorization: Bearer token used to authenticate HTTP requests to GCP APIs. This is an alternative to credentials. If both are specified, access_token will be used over the credentials field.
        :param credentials: (experimental) (Optional) Local path to Google Cloud Platform account credentials in JSON format. If unset, Google Application Default Credentials are used. The provided credentials must have Storage Object Admin role on the bucket. Warning: if using the Google Cloud Platform provider as well, it will also pick up the GOOGLE_CREDENTIALS environment variable.
        :param encryption_key: (experimental) (Optional) A 32 byte base64 encoded 'customer supplied encryption key' used to encrypt all state.
        :param impersonate_service_account: (experimental) (Optional) The service account to impersonate for accessing the State Bucket. You must have roles/iam.serviceAccountTokenCreator role on that account for the impersonation to succeed. If you are using a delegation chain, you can specify that using the impersonate_service_account_delegates field. Alternatively, this can be specified using the GOOGLE_IMPERSONATE_SERVICE_ACCOUNT environment variable.
        :param impersonate_service_account_delegates: (experimental) (Optional) The delegation chain for an impersonating a service account.
        :param prefix: (experimental) (Optional) GCS prefix inside the bucket. Named states for workspaces are stored in an object called /.tfstate.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateGcs.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateGcsConfig(
            defaults=defaults,
            workspace=workspace,
            bucket=bucket,
            access_token=access_token,
            credentials=credentials,
            encryption_key=encryption_key,
            impersonate_service_account=impersonate_service_account,
            impersonate_service_account_delegates=impersonate_service_account_delegates,
            prefix=prefix,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateGcsConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, GcsBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "bucket": "bucket",
        "access_token": "accessToken",
        "credentials": "credentials",
        "encryption_key": "encryptionKey",
        "impersonate_service_account": "impersonateServiceAccount",
        "impersonate_service_account_delegates": "impersonateServiceAccountDelegates",
        "prefix": "prefix",
    },
)
class DataTerraformRemoteStateGcsConfig(
    DataTerraformRemoteStateConfig,
    GcsBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        bucket: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        impersonate_service_account: typing.Optional[builtins.str] = None,
        impersonate_service_account_delegates: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param bucket: (experimental) (Required) The name of the GCS bucket. This name must be globally unique.
        :param access_token: (experimental) (Optional) A temporary [OAuth 2.0 access token] obtained from the Google Authorization server, i.e. the Authorization: Bearer token used to authenticate HTTP requests to GCP APIs. This is an alternative to credentials. If both are specified, access_token will be used over the credentials field.
        :param credentials: (experimental) (Optional) Local path to Google Cloud Platform account credentials in JSON format. If unset, Google Application Default Credentials are used. The provided credentials must have Storage Object Admin role on the bucket. Warning: if using the Google Cloud Platform provider as well, it will also pick up the GOOGLE_CREDENTIALS environment variable.
        :param encryption_key: (experimental) (Optional) A 32 byte base64 encoded 'customer supplied encryption key' used to encrypt all state.
        :param impersonate_service_account: (experimental) (Optional) The service account to impersonate for accessing the State Bucket. You must have roles/iam.serviceAccountTokenCreator role on that account for the impersonation to succeed. If you are using a delegation chain, you can specify that using the impersonate_service_account_delegates field. Alternatively, this can be specified using the GOOGLE_IMPERSONATE_SERVICE_ACCOUNT environment variable.
        :param impersonate_service_account_delegates: (experimental) (Optional) The delegation chain for an impersonating a service account.
        :param prefix: (experimental) (Optional) GCS prefix inside the bucket. Named states for workspaces are stored in an object called /.tfstate.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateGcsConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument impersonate_service_account", value=impersonate_service_account, expected_type=type_hints["impersonate_service_account"])
            check_type(argname="argument impersonate_service_account_delegates", value=impersonate_service_account_delegates, expected_type=type_hints["impersonate_service_account_delegates"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if access_token is not None:
            self._values["access_token"] = access_token
        if credentials is not None:
            self._values["credentials"] = credentials
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if impersonate_service_account is not None:
            self._values["impersonate_service_account"] = impersonate_service_account
        if impersonate_service_account_delegates is not None:
            self._values["impersonate_service_account_delegates"] = impersonate_service_account_delegates
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> builtins.str:
        '''(experimental) (Required) The name of the GCS bucket.

        This name must be globally unique.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A temporary [OAuth 2.0 access token] obtained from the Google Authorization server, i.e. the Authorization: Bearer token used to authenticate HTTP requests to GCP APIs. This is an alternative to credentials. If both are specified, access_token will be used over the credentials field.

        :stability: experimental
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Local path to Google Cloud Platform account credentials in JSON format.

        If unset, Google Application Default Credentials are used.
        The provided credentials must have Storage Object Admin role on the bucket.

        Warning: if using the Google Cloud Platform provider as well,
        it will also pick up the GOOGLE_CREDENTIALS environment variable.

        :stability: experimental
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) A 32 byte base64 encoded 'customer supplied encryption key' used to encrypt all state.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def impersonate_service_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The service account to impersonate for accessing the State Bucket.

        You must have roles/iam.serviceAccountTokenCreator role on that account for the impersonation to succeed.
        If you are using a delegation chain, you can specify that using the impersonate_service_account_delegates field.
        Alternatively, this can be specified using the GOOGLE_IMPERSONATE_SERVICE_ACCOUNT environment variable.

        :stability: experimental
        '''
        result = self._values.get("impersonate_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def impersonate_service_account_delegates(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) (Optional) The delegation chain for an impersonating a service account.

        :stability: experimental
        '''
        result = self._values.get("impersonate_service_account_delegates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) GCS prefix inside the bucket.

        Named states for workspaces are stored in an object called /.tfstate.

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateGcsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateHttp(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateHttp",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        address: builtins.str,
        lock_address: typing.Optional[builtins.str] = None,
        lock_method: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        retry_max: typing.Optional[jsii.Number] = None,
        retry_wait_max: typing.Optional[jsii.Number] = None,
        retry_wait_min: typing.Optional[jsii.Number] = None,
        skip_cert_verification: typing.Optional[builtins.bool] = None,
        unlock_address: typing.Optional[builtins.str] = None,
        unlock_method: typing.Optional[builtins.str] = None,
        update_method: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param address: (experimental) (Required) The address of the REST endpoint.
        :param lock_address: (experimental) (Optional) The address of the lock REST endpoint. Defaults to disabled.
        :param lock_method: (experimental) (Optional) The HTTP method to use when locking. Defaults to LOCK.
        :param password: (experimental) (Optional) The password for HTTP basic authentication.
        :param retry_max: (experimental) (Optional) The number of HTTP request retries. Defaults to 2.
        :param retry_wait_max: (experimental) (Optional) The maximum time in seconds to wait between HTTP request attempts. Defaults to 30.
        :param retry_wait_min: (experimental) (Optional) The minimum time in seconds to wait between HTTP request attempts. Defaults to 1.
        :param skip_cert_verification: (experimental) (Optional) Whether to skip TLS verification. Defaults to false.
        :param unlock_address: (experimental) (Optional) The address of the unlock REST endpoint. Defaults to disabled.
        :param unlock_method: (experimental) (Optional) The HTTP method to use when unlocking. Defaults to UNLOCK.
        :param update_method: (experimental) (Optional) HTTP method to use when updating state. Defaults to POST.
        :param username: (experimental) (Optional) The username for HTTP basic authentication.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateHttp.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateHttpConfig(
            defaults=defaults,
            workspace=workspace,
            address=address,
            lock_address=lock_address,
            lock_method=lock_method,
            password=password,
            retry_max=retry_max,
            retry_wait_max=retry_wait_max,
            retry_wait_min=retry_wait_min,
            skip_cert_verification=skip_cert_verification,
            unlock_address=unlock_address,
            unlock_method=unlock_method,
            update_method=update_method,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateHttpConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, HttpBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "address": "address",
        "lock_address": "lockAddress",
        "lock_method": "lockMethod",
        "password": "password",
        "retry_max": "retryMax",
        "retry_wait_max": "retryWaitMax",
        "retry_wait_min": "retryWaitMin",
        "skip_cert_verification": "skipCertVerification",
        "unlock_address": "unlockAddress",
        "unlock_method": "unlockMethod",
        "update_method": "updateMethod",
        "username": "username",
    },
)
class DataTerraformRemoteStateHttpConfig(
    DataTerraformRemoteStateConfig,
    HttpBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        address: builtins.str,
        lock_address: typing.Optional[builtins.str] = None,
        lock_method: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        retry_max: typing.Optional[jsii.Number] = None,
        retry_wait_max: typing.Optional[jsii.Number] = None,
        retry_wait_min: typing.Optional[jsii.Number] = None,
        skip_cert_verification: typing.Optional[builtins.bool] = None,
        unlock_address: typing.Optional[builtins.str] = None,
        unlock_method: typing.Optional[builtins.str] = None,
        update_method: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param address: (experimental) (Required) The address of the REST endpoint.
        :param lock_address: (experimental) (Optional) The address of the lock REST endpoint. Defaults to disabled.
        :param lock_method: (experimental) (Optional) The HTTP method to use when locking. Defaults to LOCK.
        :param password: (experimental) (Optional) The password for HTTP basic authentication.
        :param retry_max: (experimental) (Optional) The number of HTTP request retries. Defaults to 2.
        :param retry_wait_max: (experimental) (Optional) The maximum time in seconds to wait between HTTP request attempts. Defaults to 30.
        :param retry_wait_min: (experimental) (Optional) The minimum time in seconds to wait between HTTP request attempts. Defaults to 1.
        :param skip_cert_verification: (experimental) (Optional) Whether to skip TLS verification. Defaults to false.
        :param unlock_address: (experimental) (Optional) The address of the unlock REST endpoint. Defaults to disabled.
        :param unlock_method: (experimental) (Optional) The HTTP method to use when unlocking. Defaults to UNLOCK.
        :param update_method: (experimental) (Optional) HTTP method to use when updating state. Defaults to POST.
        :param username: (experimental) (Optional) The username for HTTP basic authentication.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateHttpConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument lock_address", value=lock_address, expected_type=type_hints["lock_address"])
            check_type(argname="argument lock_method", value=lock_method, expected_type=type_hints["lock_method"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument retry_max", value=retry_max, expected_type=type_hints["retry_max"])
            check_type(argname="argument retry_wait_max", value=retry_wait_max, expected_type=type_hints["retry_wait_max"])
            check_type(argname="argument retry_wait_min", value=retry_wait_min, expected_type=type_hints["retry_wait_min"])
            check_type(argname="argument skip_cert_verification", value=skip_cert_verification, expected_type=type_hints["skip_cert_verification"])
            check_type(argname="argument unlock_address", value=unlock_address, expected_type=type_hints["unlock_address"])
            check_type(argname="argument unlock_method", value=unlock_method, expected_type=type_hints["unlock_method"])
            check_type(argname="argument update_method", value=update_method, expected_type=type_hints["update_method"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "address": address,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if lock_address is not None:
            self._values["lock_address"] = lock_address
        if lock_method is not None:
            self._values["lock_method"] = lock_method
        if password is not None:
            self._values["password"] = password
        if retry_max is not None:
            self._values["retry_max"] = retry_max
        if retry_wait_max is not None:
            self._values["retry_wait_max"] = retry_wait_max
        if retry_wait_min is not None:
            self._values["retry_wait_min"] = retry_wait_min
        if skip_cert_verification is not None:
            self._values["skip_cert_verification"] = skip_cert_verification
        if unlock_address is not None:
            self._values["unlock_address"] = unlock_address
        if unlock_method is not None:
            self._values["unlock_method"] = unlock_method
        if update_method is not None:
            self._values["update_method"] = update_method
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address(self) -> builtins.str:
        '''(experimental) (Required) The address of the REST endpoint.

        :stability: experimental
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lock_address(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The address of the lock REST endpoint.

        Defaults to disabled.

        :stability: experimental
        '''
        result = self._values.get("lock_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_method(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The HTTP method to use when locking.

        Defaults to LOCK.

        :stability: experimental
        '''
        result = self._values.get("lock_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The password for HTTP basic authentication.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_max(self) -> typing.Optional[jsii.Number]:
        '''(experimental) (Optional) The number of HTTP request retries.

        Defaults to 2.

        :stability: experimental
        '''
        result = self._values.get("retry_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_wait_max(self) -> typing.Optional[jsii.Number]:
        '''(experimental) (Optional) The maximum time in seconds to wait between HTTP request attempts.

        Defaults to 30.

        :stability: experimental
        '''
        result = self._values.get("retry_wait_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_wait_min(self) -> typing.Optional[jsii.Number]:
        '''(experimental) (Optional) The minimum time in seconds to wait between HTTP request attempts.

        Defaults to 1.

        :stability: experimental
        '''
        result = self._values.get("retry_wait_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def skip_cert_verification(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Whether to skip TLS verification.

        Defaults to false.

        :stability: experimental
        '''
        result = self._values.get("skip_cert_verification")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def unlock_address(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The address of the unlock REST endpoint.

        Defaults to disabled.

        :stability: experimental
        '''
        result = self._values.get("unlock_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unlock_method(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The HTTP method to use when unlocking.

        Defaults to UNLOCK.

        :stability: experimental
        '''
        result = self._values.get("unlock_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_method(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) HTTP method to use when updating state.

        Defaults to POST.

        :stability: experimental
        '''
        result = self._values.get("update_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The username for HTTP basic authentication.

        :stability: experimental
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateHttpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateLocal(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateLocal",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        workspace_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param path: (experimental) Path where the state file is stored. Default: - defaults to terraform.${stackId}.tfstate
        :param workspace_dir: (experimental) (Optional) The path to non-default workspaces.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateLocal.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateLocalConfig(
            defaults=defaults,
            workspace=workspace,
            path=path,
            workspace_dir=workspace_dir,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateLocalConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, LocalBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "path": "path",
        "workspace_dir": "workspaceDir",
    },
)
class DataTerraformRemoteStateLocalConfig(
    DataTerraformRemoteStateConfig,
    LocalBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        workspace_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param path: (experimental) Path where the state file is stored. Default: - defaults to terraform.${stackId}.tfstate
        :param workspace_dir: (experimental) (Optional) The path to non-default workspaces.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateLocalConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument workspace_dir", value=workspace_dir, expected_type=type_hints["workspace_dir"])
        self._values: typing.Dict[str, typing.Any] = {}
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if path is not None:
            self._values["path"] = path
        if workspace_dir is not None:
            self._values["workspace_dir"] = workspace_dir

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path where the state file is stored.

        :default: - defaults to terraform.${stackId}.tfstate

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The path to non-default workspaces.

        :stability: experimental
        '''
        result = self._values.get("workspace_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateLocalConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateManta(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateManta",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        account: builtins.str,
        key_id: builtins.str,
        path: builtins.str,
        insecure_skip_tls_verify: typing.Optional[builtins.bool] = None,
        key_material: typing.Optional[builtins.str] = None,
        object_name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param account: 
        :param key_id: 
        :param path: 
        :param insecure_skip_tls_verify: 
        :param key_material: 
        :param object_name: 
        :param url: 
        :param user: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateManta.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateMantaConfig(
            defaults=defaults,
            workspace=workspace,
            account=account,
            key_id=key_id,
            path=path,
            insecure_skip_tls_verify=insecure_skip_tls_verify,
            key_material=key_material,
            object_name=object_name,
            url=url,
            user=user,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateMantaConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, MantaBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "account": "account",
        "key_id": "keyId",
        "path": "path",
        "insecure_skip_tls_verify": "insecureSkipTlsVerify",
        "key_material": "keyMaterial",
        "object_name": "objectName",
        "url": "url",
        "user": "user",
    },
)
class DataTerraformRemoteStateMantaConfig(
    DataTerraformRemoteStateConfig,
    MantaBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        account: builtins.str,
        key_id: builtins.str,
        path: builtins.str,
        insecure_skip_tls_verify: typing.Optional[builtins.bool] = None,
        key_material: typing.Optional[builtins.str] = None,
        object_name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param account: 
        :param key_id: 
        :param path: 
        :param insecure_skip_tls_verify: 
        :param key_material: 
        :param object_name: 
        :param url: 
        :param user: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateMantaConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument insecure_skip_tls_verify", value=insecure_skip_tls_verify, expected_type=type_hints["insecure_skip_tls_verify"])
            check_type(argname="argument key_material", value=key_material, expected_type=type_hints["key_material"])
            check_type(argname="argument object_name", value=object_name, expected_type=type_hints["object_name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "key_id": key_id,
            "path": path,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if insecure_skip_tls_verify is not None:
            self._values["insecure_skip_tls_verify"] = insecure_skip_tls_verify
        if key_material is not None:
            self._values["key_material"] = key_material
        if object_name is not None:
            self._values["object_name"] = object_name
        if url is not None:
            self._values["url"] = url
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("key_id")
        assert result is not None, "Required property 'key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def insecure_skip_tls_verify(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("insecure_skip_tls_verify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_material(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("object_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateMantaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateOss(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateOss",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        bucket: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        assume_role: typing.Optional[typing.Union[OssAssumeRole, typing.Dict[str, typing.Any]]] = None,
        ecs_role_name: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        security_token: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        tablestore_endpoint: typing.Optional[builtins.str] = None,
        tablestore_table: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param access_key: 
        :param acl: 
        :param assume_role: 
        :param ecs_role_name: 
        :param encrypt: 
        :param endpoint: 
        :param key: 
        :param prefix: 
        :param profile: 
        :param region: 
        :param secret_key: 
        :param security_token: 
        :param shared_credentials_file: 
        :param tablestore_endpoint: 
        :param tablestore_table: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateOss.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateOssConfig(
            defaults=defaults,
            workspace=workspace,
            bucket=bucket,
            access_key=access_key,
            acl=acl,
            assume_role=assume_role,
            ecs_role_name=ecs_role_name,
            encrypt=encrypt,
            endpoint=endpoint,
            key=key,
            prefix=prefix,
            profile=profile,
            region=region,
            secret_key=secret_key,
            security_token=security_token,
            shared_credentials_file=shared_credentials_file,
            tablestore_endpoint=tablestore_endpoint,
            tablestore_table=tablestore_table,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateOssConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, OssBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "bucket": "bucket",
        "access_key": "accessKey",
        "acl": "acl",
        "assume_role": "assumeRole",
        "ecs_role_name": "ecsRoleName",
        "encrypt": "encrypt",
        "endpoint": "endpoint",
        "key": "key",
        "prefix": "prefix",
        "profile": "profile",
        "region": "region",
        "secret_key": "secretKey",
        "security_token": "securityToken",
        "shared_credentials_file": "sharedCredentialsFile",
        "tablestore_endpoint": "tablestoreEndpoint",
        "tablestore_table": "tablestoreTable",
    },
)
class DataTerraformRemoteStateOssConfig(
    DataTerraformRemoteStateConfig,
    OssBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        bucket: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        assume_role: typing.Optional[typing.Union[OssAssumeRole, typing.Dict[str, typing.Any]]] = None,
        ecs_role_name: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        security_token: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        tablestore_endpoint: typing.Optional[builtins.str] = None,
        tablestore_table: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param access_key: 
        :param acl: 
        :param assume_role: 
        :param ecs_role_name: 
        :param encrypt: 
        :param endpoint: 
        :param key: 
        :param prefix: 
        :param profile: 
        :param region: 
        :param secret_key: 
        :param security_token: 
        :param shared_credentials_file: 
        :param tablestore_endpoint: 
        :param tablestore_table: 

        :stability: experimental
        '''
        if isinstance(assume_role, dict):
            assume_role = OssAssumeRole(**assume_role)
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateOssConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument assume_role", value=assume_role, expected_type=type_hints["assume_role"])
            check_type(argname="argument ecs_role_name", value=ecs_role_name, expected_type=type_hints["ecs_role_name"])
            check_type(argname="argument encrypt", value=encrypt, expected_type=type_hints["encrypt"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument security_token", value=security_token, expected_type=type_hints["security_token"])
            check_type(argname="argument shared_credentials_file", value=shared_credentials_file, expected_type=type_hints["shared_credentials_file"])
            check_type(argname="argument tablestore_endpoint", value=tablestore_endpoint, expected_type=type_hints["tablestore_endpoint"])
            check_type(argname="argument tablestore_table", value=tablestore_table, expected_type=type_hints["tablestore_table"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if ecs_role_name is not None:
            self._values["ecs_role_name"] = ecs_role_name
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if security_token is not None:
            self._values["security_token"] = security_token
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if tablestore_endpoint is not None:
            self._values["tablestore_endpoint"] = tablestore_endpoint
        if tablestore_table is not None:
            self._values["tablestore_table"] = tablestore_table

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role(self) -> typing.Optional[OssAssumeRole]:
        '''
        :stability: experimental
        '''
        result = self._values.get("assume_role")
        return typing.cast(typing.Optional[OssAssumeRole], result)

    @builtins.property
    def ecs_role_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ecs_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypt(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("encrypt")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("shared_credentials_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tablestore_endpoint(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tablestore_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tablestore_table(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tablestore_table")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateOssConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStatePg(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStatePg",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        conn_str: builtins.str,
        schema_name: typing.Optional[builtins.str] = None,
        skip_schema_creation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param conn_str: 
        :param schema_name: 
        :param skip_schema_creation: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStatePg.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStatePgConfig(
            defaults=defaults,
            workspace=workspace,
            conn_str=conn_str,
            schema_name=schema_name,
            skip_schema_creation=skip_schema_creation,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStatePgConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, PgBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "conn_str": "connStr",
        "schema_name": "schemaName",
        "skip_schema_creation": "skipSchemaCreation",
    },
)
class DataTerraformRemoteStatePgConfig(DataTerraformRemoteStateConfig, PgBackendProps):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        conn_str: builtins.str,
        schema_name: typing.Optional[builtins.str] = None,
        skip_schema_creation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param conn_str: 
        :param schema_name: 
        :param skip_schema_creation: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStatePgConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument conn_str", value=conn_str, expected_type=type_hints["conn_str"])
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument skip_schema_creation", value=skip_schema_creation, expected_type=type_hints["skip_schema_creation"])
        self._values: typing.Dict[str, typing.Any] = {
            "conn_str": conn_str,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if schema_name is not None:
            self._values["schema_name"] = schema_name
        if skip_schema_creation is not None:
            self._values["skip_schema_creation"] = skip_schema_creation

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conn_str(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("conn_str")
        assert result is not None, "Required property 'conn_str' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_schema_creation(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_schema_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStatePgConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateRemoteConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, RemoteBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "organization": "organization",
        "workspaces": "workspaces",
        "hostname": "hostname",
        "token": "token",
    },
)
class DataTerraformRemoteStateRemoteConfig(
    DataTerraformRemoteStateConfig,
    RemoteBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        organization: builtins.str,
        workspaces: IRemoteWorkspace,
        hostname: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateRemoteConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument workspaces", value=workspaces, expected_type=type_hints["workspaces"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[str, typing.Any] = {
            "organization": organization,
            "workspaces": workspaces,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if hostname is not None:
            self._values["hostname"] = hostname
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspaces(self) -> IRemoteWorkspace:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspaces")
        assert result is not None, "Required property 'workspaces' is missing"
        return typing.cast(IRemoteWorkspace, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateRemoteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateS3(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateS3",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        bucket: builtins.str,
        key: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        assume_role_policy: typing.Optional[builtins.str] = None,
        assume_role_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        assume_role_transitive_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        dynamodb_endpoint: typing.Optional[builtins.str] = None,
        dynamodb_table: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        force_path_style: typing.Optional[builtins.bool] = None,
        iam_endpoint: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        session_name: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        skip_credentials_validation: typing.Optional[builtins.bool] = None,
        skip_metadata_api_check: typing.Optional[builtins.bool] = None,
        skip_region_validation: typing.Optional[builtins.bool] = None,
        sse_customer_key: typing.Optional[builtins.str] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        workspace_key_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param bucket: (experimental) Name of the S3 Bucket.
        :param key: (experimental) Path to the state file inside the S3 Bucket. When using a non-default workspace, the state path will be /workspace_key_prefix/workspace_name/key
        :param access_key: (experimental) (Optional) AWS access key. If configured, must also configure secret_key. This can also be sourced from the AWS_ACCESS_KEY_ID environment variable, AWS shared credentials file (e.g. ~/.aws/credentials), or AWS shared configuration file (e.g. ~/.aws/config).
        :param acl: (experimental) (Optional) Canned ACL to be applied to the state file.
        :param assume_role_policy: (experimental) (Optional) IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.
        :param assume_role_policy_arns: (experimental) (Optional) Set of Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.
        :param assume_role_tags: (experimental) (Optional) Map of assume role session tags.
        :param assume_role_transitive_tag_keys: (experimental) (Optional) Set of assume role session tag keys to pass to any subsequent sessions.
        :param dynamodb_endpoint: (experimental) (Optional) Custom endpoint for the AWS DynamoDB API. This can also be sourced from the AWS_DYNAMODB_ENDPOINT environment variable.
        :param dynamodb_table: (experimental) (Optional) Name of DynamoDB Table to use for state locking and consistency. The table must have a partition key named LockID with type of String. If not configured, state locking will be disabled.
        :param encrypt: (experimental) (Optional) Enable server side encryption of the state file.
        :param endpoint: (experimental) (Optional) Custom endpoint for the AWS S3 API. This can also be sourced from the AWS_S3_ENDPOINT environment variable.
        :param external_id: (experimental) (Optional) External identifier to use when assuming the role.
        :param force_path_style: (experimental) (Optional) Enable path-style S3 URLs (https:/// instead of https://.).
        :param iam_endpoint: (experimental) (Optional) Custom endpoint for the AWS Identity and Access Management (IAM) API. This can also be sourced from the AWS_IAM_ENDPOINT environment variable.
        :param kms_key_id: (experimental) (Optional) Amazon Resource Name (ARN) of a Key Management Service (KMS) Key to use for encrypting the state. Note that if this value is specified, Terraform will need kms:Encrypt, kms:Decrypt and kms:GenerateDataKey permissions on this KMS key.
        :param max_retries: (experimental) (Optional) The maximum number of times an AWS API request is retried on retryable failure. Defaults to 5.
        :param profile: (experimental) (Optional) Name of AWS profile in AWS shared credentials file (e.g. ~/.aws/credentials) or AWS shared configuration file (e.g. ~/.aws/config) to use for credentials and/or configuration. This can also be sourced from the AWS_PROFILE environment variable.
        :param region: (experimental) AWS Region of the S3 Bucket and DynamoDB Table (if used). This can also be sourced from the AWS_DEFAULT_REGION and AWS_REGION environment variables.
        :param role_arn: (experimental) (Optional) Amazon Resource Name (ARN) of the IAM Role to assume.
        :param secret_key: (experimental) (Optional) AWS secret access key. If configured, must also configure access_key. This can also be sourced from the AWS_SECRET_ACCESS_KEY environment variable, AWS shared credentials file (e.g. ~/.aws/credentials), or AWS shared configuration file (e.g. ~/.aws/config)
        :param session_name: (experimental) (Optional) Session name to use when assuming the role.
        :param shared_credentials_file: (experimental) (Optional) Path to the AWS shared credentials file. Defaults to ~/.aws/credentials.
        :param skip_credentials_validation: (experimental) (Optional) Skip credentials validation via the STS API.
        :param skip_metadata_api_check: (experimental) (Optional) Skip usage of EC2 Metadata API.
        :param skip_region_validation: (experimental) (Optional) Skip validation of provided region name.
        :param sse_customer_key: (experimental) (Optional) The key to use for encrypting state with Server-Side Encryption with Customer-Provided Keys (SSE-C). This is the base64-encoded value of the key, which must decode to 256 bits. This can also be sourced from the AWS_SSE_CUSTOMER_KEY environment variable, which is recommended due to the sensitivity of the value. Setting it inside a terraform file will cause it to be persisted to disk in terraform.tfstate.
        :param sts_endpoint: (experimental) (Optional) Custom endpoint for the AWS Security Token Service (STS) API. This can also be sourced from the AWS_STS_ENDPOINT environment variable.
        :param token: (experimental) (Optional) Multi-Factor Authentication (MFA) token. This can also be sourced from the AWS_SESSION_TOKEN environment variable.
        :param workspace_key_prefix: (experimental) (Optional) Prefix applied to the state path inside the bucket. This is only relevant when using a non-default workspace. Defaults to env:

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateS3.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateS3Config(
            defaults=defaults,
            workspace=workspace,
            bucket=bucket,
            key=key,
            access_key=access_key,
            acl=acl,
            assume_role_policy=assume_role_policy,
            assume_role_policy_arns=assume_role_policy_arns,
            assume_role_tags=assume_role_tags,
            assume_role_transitive_tag_keys=assume_role_transitive_tag_keys,
            dynamodb_endpoint=dynamodb_endpoint,
            dynamodb_table=dynamodb_table,
            encrypt=encrypt,
            endpoint=endpoint,
            external_id=external_id,
            force_path_style=force_path_style,
            iam_endpoint=iam_endpoint,
            kms_key_id=kms_key_id,
            max_retries=max_retries,
            profile=profile,
            region=region,
            role_arn=role_arn,
            secret_key=secret_key,
            session_name=session_name,
            shared_credentials_file=shared_credentials_file,
            skip_credentials_validation=skip_credentials_validation,
            skip_metadata_api_check=skip_metadata_api_check,
            skip_region_validation=skip_region_validation,
            sse_customer_key=sse_customer_key,
            sts_endpoint=sts_endpoint,
            token=token,
            workspace_key_prefix=workspace_key_prefix,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateS3Config",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, S3BackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "bucket": "bucket",
        "key": "key",
        "access_key": "accessKey",
        "acl": "acl",
        "assume_role_policy": "assumeRolePolicy",
        "assume_role_policy_arns": "assumeRolePolicyArns",
        "assume_role_tags": "assumeRoleTags",
        "assume_role_transitive_tag_keys": "assumeRoleTransitiveTagKeys",
        "dynamodb_endpoint": "dynamodbEndpoint",
        "dynamodb_table": "dynamodbTable",
        "encrypt": "encrypt",
        "endpoint": "endpoint",
        "external_id": "externalId",
        "force_path_style": "forcePathStyle",
        "iam_endpoint": "iamEndpoint",
        "kms_key_id": "kmsKeyId",
        "max_retries": "maxRetries",
        "profile": "profile",
        "region": "region",
        "role_arn": "roleArn",
        "secret_key": "secretKey",
        "session_name": "sessionName",
        "shared_credentials_file": "sharedCredentialsFile",
        "skip_credentials_validation": "skipCredentialsValidation",
        "skip_metadata_api_check": "skipMetadataApiCheck",
        "skip_region_validation": "skipRegionValidation",
        "sse_customer_key": "sseCustomerKey",
        "sts_endpoint": "stsEndpoint",
        "token": "token",
        "workspace_key_prefix": "workspaceKeyPrefix",
    },
)
class DataTerraformRemoteStateS3Config(DataTerraformRemoteStateConfig, S3BackendProps):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        bucket: builtins.str,
        key: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        assume_role_policy: typing.Optional[builtins.str] = None,
        assume_role_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        assume_role_transitive_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        dynamodb_endpoint: typing.Optional[builtins.str] = None,
        dynamodb_table: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        force_path_style: typing.Optional[builtins.bool] = None,
        iam_endpoint: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        session_name: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        skip_credentials_validation: typing.Optional[builtins.bool] = None,
        skip_metadata_api_check: typing.Optional[builtins.bool] = None,
        skip_region_validation: typing.Optional[builtins.bool] = None,
        sse_customer_key: typing.Optional[builtins.str] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        workspace_key_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param bucket: (experimental) Name of the S3 Bucket.
        :param key: (experimental) Path to the state file inside the S3 Bucket. When using a non-default workspace, the state path will be /workspace_key_prefix/workspace_name/key
        :param access_key: (experimental) (Optional) AWS access key. If configured, must also configure secret_key. This can also be sourced from the AWS_ACCESS_KEY_ID environment variable, AWS shared credentials file (e.g. ~/.aws/credentials), or AWS shared configuration file (e.g. ~/.aws/config).
        :param acl: (experimental) (Optional) Canned ACL to be applied to the state file.
        :param assume_role_policy: (experimental) (Optional) IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.
        :param assume_role_policy_arns: (experimental) (Optional) Set of Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.
        :param assume_role_tags: (experimental) (Optional) Map of assume role session tags.
        :param assume_role_transitive_tag_keys: (experimental) (Optional) Set of assume role session tag keys to pass to any subsequent sessions.
        :param dynamodb_endpoint: (experimental) (Optional) Custom endpoint for the AWS DynamoDB API. This can also be sourced from the AWS_DYNAMODB_ENDPOINT environment variable.
        :param dynamodb_table: (experimental) (Optional) Name of DynamoDB Table to use for state locking and consistency. The table must have a partition key named LockID with type of String. If not configured, state locking will be disabled.
        :param encrypt: (experimental) (Optional) Enable server side encryption of the state file.
        :param endpoint: (experimental) (Optional) Custom endpoint for the AWS S3 API. This can also be sourced from the AWS_S3_ENDPOINT environment variable.
        :param external_id: (experimental) (Optional) External identifier to use when assuming the role.
        :param force_path_style: (experimental) (Optional) Enable path-style S3 URLs (https:/// instead of https://.).
        :param iam_endpoint: (experimental) (Optional) Custom endpoint for the AWS Identity and Access Management (IAM) API. This can also be sourced from the AWS_IAM_ENDPOINT environment variable.
        :param kms_key_id: (experimental) (Optional) Amazon Resource Name (ARN) of a Key Management Service (KMS) Key to use for encrypting the state. Note that if this value is specified, Terraform will need kms:Encrypt, kms:Decrypt and kms:GenerateDataKey permissions on this KMS key.
        :param max_retries: (experimental) (Optional) The maximum number of times an AWS API request is retried on retryable failure. Defaults to 5.
        :param profile: (experimental) (Optional) Name of AWS profile in AWS shared credentials file (e.g. ~/.aws/credentials) or AWS shared configuration file (e.g. ~/.aws/config) to use for credentials and/or configuration. This can also be sourced from the AWS_PROFILE environment variable.
        :param region: (experimental) AWS Region of the S3 Bucket and DynamoDB Table (if used). This can also be sourced from the AWS_DEFAULT_REGION and AWS_REGION environment variables.
        :param role_arn: (experimental) (Optional) Amazon Resource Name (ARN) of the IAM Role to assume.
        :param secret_key: (experimental) (Optional) AWS secret access key. If configured, must also configure access_key. This can also be sourced from the AWS_SECRET_ACCESS_KEY environment variable, AWS shared credentials file (e.g. ~/.aws/credentials), or AWS shared configuration file (e.g. ~/.aws/config)
        :param session_name: (experimental) (Optional) Session name to use when assuming the role.
        :param shared_credentials_file: (experimental) (Optional) Path to the AWS shared credentials file. Defaults to ~/.aws/credentials.
        :param skip_credentials_validation: (experimental) (Optional) Skip credentials validation via the STS API.
        :param skip_metadata_api_check: (experimental) (Optional) Skip usage of EC2 Metadata API.
        :param skip_region_validation: (experimental) (Optional) Skip validation of provided region name.
        :param sse_customer_key: (experimental) (Optional) The key to use for encrypting state with Server-Side Encryption with Customer-Provided Keys (SSE-C). This is the base64-encoded value of the key, which must decode to 256 bits. This can also be sourced from the AWS_SSE_CUSTOMER_KEY environment variable, which is recommended due to the sensitivity of the value. Setting it inside a terraform file will cause it to be persisted to disk in terraform.tfstate.
        :param sts_endpoint: (experimental) (Optional) Custom endpoint for the AWS Security Token Service (STS) API. This can also be sourced from the AWS_STS_ENDPOINT environment variable.
        :param token: (experimental) (Optional) Multi-Factor Authentication (MFA) token. This can also be sourced from the AWS_SESSION_TOKEN environment variable.
        :param workspace_key_prefix: (experimental) (Optional) Prefix applied to the state path inside the bucket. This is only relevant when using a non-default workspace. Defaults to env:

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateS3Config.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument assume_role_policy", value=assume_role_policy, expected_type=type_hints["assume_role_policy"])
            check_type(argname="argument assume_role_policy_arns", value=assume_role_policy_arns, expected_type=type_hints["assume_role_policy_arns"])
            check_type(argname="argument assume_role_tags", value=assume_role_tags, expected_type=type_hints["assume_role_tags"])
            check_type(argname="argument assume_role_transitive_tag_keys", value=assume_role_transitive_tag_keys, expected_type=type_hints["assume_role_transitive_tag_keys"])
            check_type(argname="argument dynamodb_endpoint", value=dynamodb_endpoint, expected_type=type_hints["dynamodb_endpoint"])
            check_type(argname="argument dynamodb_table", value=dynamodb_table, expected_type=type_hints["dynamodb_table"])
            check_type(argname="argument encrypt", value=encrypt, expected_type=type_hints["encrypt"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument force_path_style", value=force_path_style, expected_type=type_hints["force_path_style"])
            check_type(argname="argument iam_endpoint", value=iam_endpoint, expected_type=type_hints["iam_endpoint"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
            check_type(argname="argument shared_credentials_file", value=shared_credentials_file, expected_type=type_hints["shared_credentials_file"])
            check_type(argname="argument skip_credentials_validation", value=skip_credentials_validation, expected_type=type_hints["skip_credentials_validation"])
            check_type(argname="argument skip_metadata_api_check", value=skip_metadata_api_check, expected_type=type_hints["skip_metadata_api_check"])
            check_type(argname="argument skip_region_validation", value=skip_region_validation, expected_type=type_hints["skip_region_validation"])
            check_type(argname="argument sse_customer_key", value=sse_customer_key, expected_type=type_hints["sse_customer_key"])
            check_type(argname="argument sts_endpoint", value=sts_endpoint, expected_type=type_hints["sts_endpoint"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument workspace_key_prefix", value=workspace_key_prefix, expected_type=type_hints["workspace_key_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "key": key,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if assume_role_policy is not None:
            self._values["assume_role_policy"] = assume_role_policy
        if assume_role_policy_arns is not None:
            self._values["assume_role_policy_arns"] = assume_role_policy_arns
        if assume_role_tags is not None:
            self._values["assume_role_tags"] = assume_role_tags
        if assume_role_transitive_tag_keys is not None:
            self._values["assume_role_transitive_tag_keys"] = assume_role_transitive_tag_keys
        if dynamodb_endpoint is not None:
            self._values["dynamodb_endpoint"] = dynamodb_endpoint
        if dynamodb_table is not None:
            self._values["dynamodb_table"] = dynamodb_table
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if external_id is not None:
            self._values["external_id"] = external_id
        if force_path_style is not None:
            self._values["force_path_style"] = force_path_style
        if iam_endpoint is not None:
            self._values["iam_endpoint"] = iam_endpoint
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if session_name is not None:
            self._values["session_name"] = session_name
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if skip_credentials_validation is not None:
            self._values["skip_credentials_validation"] = skip_credentials_validation
        if skip_metadata_api_check is not None:
            self._values["skip_metadata_api_check"] = skip_metadata_api_check
        if skip_region_validation is not None:
            self._values["skip_region_validation"] = skip_region_validation
        if sse_customer_key is not None:
            self._values["sse_customer_key"] = sse_customer_key
        if sts_endpoint is not None:
            self._values["sts_endpoint"] = sts_endpoint
        if token is not None:
            self._values["token"] = token
        if workspace_key_prefix is not None:
            self._values["workspace_key_prefix"] = workspace_key_prefix

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> builtins.str:
        '''(experimental) Name of the S3 Bucket.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) Path to the state file inside the S3 Bucket.

        When using a non-default workspace, the state path will be /workspace_key_prefix/workspace_name/key

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) AWS access key.

        If configured, must also configure secret_key.
        This can also be sourced from
        the AWS_ACCESS_KEY_ID environment variable,
        AWS shared credentials file (e.g. ~/.aws/credentials),
        or AWS shared configuration file (e.g. ~/.aws/config).

        :stability: experimental
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Canned ACL to be applied to the state file.

        :stability: experimental
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role_policy(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.

        :stability: experimental
        '''
        result = self._values.get("assume_role_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) (Optional) Set of Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.

        :stability: experimental
        '''
        result = self._values.get("assume_role_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assume_role_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) (Optional) Map of assume role session tags.

        :stability: experimental
        '''
        result = self._values.get("assume_role_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def assume_role_transitive_tag_keys(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) (Optional) Set of assume role session tag keys to pass to any subsequent sessions.

        :stability: experimental
        '''
        result = self._values.get("assume_role_transitive_tag_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dynamodb_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Custom endpoint for the AWS DynamoDB API.

        This can also be sourced from the AWS_DYNAMODB_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("dynamodb_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb_table(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Name of DynamoDB Table to use for state locking and consistency.

        The table must have a partition key named LockID with type of String.
        If not configured, state locking will be disabled.

        :stability: experimental
        '''
        result = self._values.get("dynamodb_table")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypt(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Enable server side encryption of the state file.

        :stability: experimental
        '''
        result = self._values.get("encrypt")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Custom endpoint for the AWS S3 API.

        This can also be sourced from the AWS_S3_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) External identifier to use when assuming the role.

        :stability: experimental
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_path_style(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Enable path-style S3 URLs (https:/// instead of https://.).

        :stability: experimental
        '''
        result = self._values.get("force_path_style")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iam_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Custom endpoint for the AWS Identity and Access Management (IAM) API.

        This can also be sourced from the AWS_IAM_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("iam_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Amazon Resource Name (ARN) of a Key Management Service (KMS) Key to use for encrypting the state.

        Note that if this value is specified,
        Terraform will need kms:Encrypt, kms:Decrypt and kms:GenerateDataKey permissions on this KMS key.

        :stability: experimental
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''(experimental) (Optional) The maximum number of times an AWS API request is retried on retryable failure.

        Defaults to 5.

        :stability: experimental
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Name of AWS profile in AWS shared credentials file (e.g. ~/.aws/credentials) or AWS shared configuration file (e.g. ~/.aws/config) to use for credentials and/or configuration. This can also be sourced from the AWS_PROFILE environment variable.

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) AWS Region of the S3 Bucket and DynamoDB Table (if used).

        This can also
        be sourced from the AWS_DEFAULT_REGION and AWS_REGION environment
        variables.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Amazon Resource Name (ARN) of the IAM Role to assume.

        :stability: experimental
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) AWS secret access key.

        If configured, must also configure access_key.
        This can also be sourced from
        the AWS_SECRET_ACCESS_KEY environment variable,
        AWS shared credentials file (e.g. ~/.aws/credentials),
        or AWS shared configuration file (e.g. ~/.aws/config)

        :stability: experimental
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Session name to use when assuming the role.

        :stability: experimental
        '''
        result = self._values.get("session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Path to the AWS shared credentials file.

        Defaults to ~/.aws/credentials.

        :stability: experimental
        '''
        result = self._values.get("shared_credentials_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_credentials_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Skip credentials validation via the STS API.

        :stability: experimental
        '''
        result = self._values.get("skip_credentials_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skip_metadata_api_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Skip usage of EC2 Metadata API.

        :stability: experimental
        '''
        result = self._values.get("skip_metadata_api_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skip_region_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) (Optional) Skip validation of provided region name.

        :stability: experimental
        '''
        result = self._values.get("skip_region_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sse_customer_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) The key to use for encrypting state with Server-Side Encryption with Customer-Provided Keys (SSE-C).

        This is the base64-encoded value of the key, which must decode to 256 bits.
        This can also be sourced from the AWS_SSE_CUSTOMER_KEY environment variable,
        which is recommended due to the sensitivity of the value.
        Setting it inside a terraform file will cause it to be persisted to disk in terraform.tfstate.

        :stability: experimental
        '''
        result = self._values.get("sse_customer_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Custom endpoint for the AWS Security Token Service (STS) API.

        This can also be sourced from the AWS_STS_ENDPOINT environment variable.

        :stability: experimental
        '''
        result = self._values.get("sts_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Multi-Factor Authentication (MFA) token.

        This can also be sourced from the AWS_SESSION_TOKEN environment variable.

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_key_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) (Optional) Prefix applied to the state path inside the bucket.

        This is only relevant when using a non-default workspace. Defaults to env:

        :stability: experimental
        '''
        result = self._values.get("workspace_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateS3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateSwift(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateSwift",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        container: builtins.str,
        application_credential_id: typing.Optional[builtins.str] = None,
        application_credential_name: typing.Optional[builtins.str] = None,
        application_credential_secret: typing.Optional[builtins.str] = None,
        archive_container: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        default_domain: typing.Optional[builtins.str] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        expire_after: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        project_domain_id: typing.Optional[builtins.str] = None,
        project_domain_name: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        state_name: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_domain_id: typing.Optional[builtins.str] = None,
        user_domain_name: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param container: 
        :param application_credential_id: 
        :param application_credential_name: 
        :param application_credential_secret: 
        :param archive_container: 
        :param auth_url: 
        :param cacert_file: 
        :param cert: 
        :param cloud: 
        :param default_domain: 
        :param domain_id: 
        :param domain_name: 
        :param expire_after: 
        :param insecure: 
        :param key: 
        :param password: 
        :param project_domain_id: 
        :param project_domain_name: 
        :param region_name: 
        :param state_name: 
        :param tenant_id: 
        :param tenant_name: 
        :param token: 
        :param user_domain_id: 
        :param user_domain_name: 
        :param user_id: 
        :param user_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateSwift.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataTerraformRemoteStateSwiftConfig(
            defaults=defaults,
            workspace=workspace,
            container=container,
            application_credential_id=application_credential_id,
            application_credential_name=application_credential_name,
            application_credential_secret=application_credential_secret,
            archive_container=archive_container,
            auth_url=auth_url,
            cacert_file=cacert_file,
            cert=cert,
            cloud=cloud,
            default_domain=default_domain,
            domain_id=domain_id,
            domain_name=domain_name,
            expire_after=expire_after,
            insecure=insecure,
            key=key,
            password=password,
            project_domain_id=project_domain_id,
            project_domain_name=project_domain_name,
            region_name=region_name,
            state_name=state_name,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            token=token,
            user_domain_id=user_domain_id,
            user_domain_name=user_domain_name,
            user_id=user_id,
            user_name=user_name,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateSwiftConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, SwiftBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "container": "container",
        "application_credential_id": "applicationCredentialId",
        "application_credential_name": "applicationCredentialName",
        "application_credential_secret": "applicationCredentialSecret",
        "archive_container": "archiveContainer",
        "auth_url": "authUrl",
        "cacert_file": "cacertFile",
        "cert": "cert",
        "cloud": "cloud",
        "default_domain": "defaultDomain",
        "domain_id": "domainId",
        "domain_name": "domainName",
        "expire_after": "expireAfter",
        "insecure": "insecure",
        "key": "key",
        "password": "password",
        "project_domain_id": "projectDomainId",
        "project_domain_name": "projectDomainName",
        "region_name": "regionName",
        "state_name": "stateName",
        "tenant_id": "tenantId",
        "tenant_name": "tenantName",
        "token": "token",
        "user_domain_id": "userDomainId",
        "user_domain_name": "userDomainName",
        "user_id": "userId",
        "user_name": "userName",
    },
)
class DataTerraformRemoteStateSwiftConfig(
    DataTerraformRemoteStateConfig,
    SwiftBackendProps,
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workspace: typing.Optional[builtins.str] = None,
        container: builtins.str,
        application_credential_id: typing.Optional[builtins.str] = None,
        application_credential_name: typing.Optional[builtins.str] = None,
        application_credential_secret: typing.Optional[builtins.str] = None,
        archive_container: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        default_domain: typing.Optional[builtins.str] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        expire_after: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        project_domain_id: typing.Optional[builtins.str] = None,
        project_domain_name: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        state_name: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_domain_id: typing.Optional[builtins.str] = None,
        user_domain_name: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param defaults: 
        :param workspace: 
        :param container: 
        :param application_credential_id: 
        :param application_credential_name: 
        :param application_credential_secret: 
        :param archive_container: 
        :param auth_url: 
        :param cacert_file: 
        :param cert: 
        :param cloud: 
        :param default_domain: 
        :param domain_id: 
        :param domain_name: 
        :param expire_after: 
        :param insecure: 
        :param key: 
        :param password: 
        :param project_domain_id: 
        :param project_domain_name: 
        :param region_name: 
        :param state_name: 
        :param tenant_id: 
        :param tenant_name: 
        :param token: 
        :param user_domain_id: 
        :param user_domain_name: 
        :param user_id: 
        :param user_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataTerraformRemoteStateSwiftConfig.__init__)
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument application_credential_id", value=application_credential_id, expected_type=type_hints["application_credential_id"])
            check_type(argname="argument application_credential_name", value=application_credential_name, expected_type=type_hints["application_credential_name"])
            check_type(argname="argument application_credential_secret", value=application_credential_secret, expected_type=type_hints["application_credential_secret"])
            check_type(argname="argument archive_container", value=archive_container, expected_type=type_hints["archive_container"])
            check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
            check_type(argname="argument cacert_file", value=cacert_file, expected_type=type_hints["cacert_file"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument cloud", value=cloud, expected_type=type_hints["cloud"])
            check_type(argname="argument default_domain", value=default_domain, expected_type=type_hints["default_domain"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument expire_after", value=expire_after, expected_type=type_hints["expire_after"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument project_domain_id", value=project_domain_id, expected_type=type_hints["project_domain_id"])
            check_type(argname="argument project_domain_name", value=project_domain_name, expected_type=type_hints["project_domain_name"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument state_name", value=state_name, expected_type=type_hints["state_name"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument tenant_name", value=tenant_name, expected_type=type_hints["tenant_name"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument user_domain_id", value=user_domain_id, expected_type=type_hints["user_domain_id"])
            check_type(argname="argument user_domain_name", value=user_domain_name, expected_type=type_hints["user_domain_name"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "container": container,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if application_credential_id is not None:
            self._values["application_credential_id"] = application_credential_id
        if application_credential_name is not None:
            self._values["application_credential_name"] = application_credential_name
        if application_credential_secret is not None:
            self._values["application_credential_secret"] = application_credential_secret
        if archive_container is not None:
            self._values["archive_container"] = archive_container
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if cacert_file is not None:
            self._values["cacert_file"] = cacert_file
        if cert is not None:
            self._values["cert"] = cert
        if cloud is not None:
            self._values["cloud"] = cloud
        if default_domain is not None:
            self._values["default_domain"] = default_domain
        if domain_id is not None:
            self._values["domain_id"] = domain_id
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if expire_after is not None:
            self._values["expire_after"] = expire_after
        if insecure is not None:
            self._values["insecure"] = insecure
        if key is not None:
            self._values["key"] = key
        if password is not None:
            self._values["password"] = password
        if project_domain_id is not None:
            self._values["project_domain_id"] = project_domain_id
        if project_domain_name is not None:
            self._values["project_domain_name"] = project_domain_name
        if region_name is not None:
            self._values["region_name"] = region_name
        if state_name is not None:
            self._values["state_name"] = state_name
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if tenant_name is not None:
            self._values["tenant_name"] = tenant_name
        if token is not None:
            self._values["token"] = token
        if user_domain_id is not None:
            self._values["user_domain_id"] = user_domain_id
        if user_domain_name is not None:
            self._values["user_domain_name"] = user_domain_name
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_credential_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("application_credential_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_credential_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("application_credential_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_credential_secret(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("application_credential_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def archive_container(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("archive_container")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cacert_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cacert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cloud")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_domain(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expire_after(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("expire_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("project_domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("project_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("region_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("state_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("tenant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateSwiftConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITokenResolver)
class DefaultTokenResolver(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DefaultTokenResolver",
):
    '''(experimental) Default resolver implementation.

    :stability: experimental
    '''

    def __init__(self, concat: IFragmentConcatenator) -> None:
        '''(experimental) Resolves tokens.

        :param concat: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DefaultTokenResolver.__init__)
            check_type(argname="argument concat", value=concat, expected_type=type_hints["concat"])
        jsii.create(self.__class__, self, [concat])

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self,
        xs: typing.Sequence[builtins.str],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolves a list of string.

        :param xs: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DefaultTokenResolver.resolve_list)
            check_type(argname="argument xs", value=xs, expected_type=type_hints["xs"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveList", [xs, context]))

    @jsii.member(jsii_name="resolveMap")
    def resolve_map(
        self,
        xs: typing.Mapping[builtins.str, typing.Any],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolves a map token.

        :param xs: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DefaultTokenResolver.resolve_map)
            check_type(argname="argument xs", value=xs, expected_type=type_hints["xs"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveMap", [xs, context]))

    @jsii.member(jsii_name="resolveNumberList")
    def resolve_number_list(
        self,
        xs: typing.Sequence[jsii.Number],
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolves a list of numbers.

        :param xs: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DefaultTokenResolver.resolve_number_list)
            check_type(argname="argument xs", value=xs, expected_type=type_hints["xs"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveNumberList", [xs, context]))

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self,
        fragments: TokenizedStringFragments,
        context: IResolveContext,
    ) -> typing.Any:
        '''(experimental) Resolve string fragments to Tokens.

        :param fragments: -
        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DefaultTokenResolver.resolve_string)
            check_type(argname="argument fragments", value=fragments, expected_type=type_hints["fragments"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveString", [fragments, context]))

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: IResolvable,
        context: IResolveContext,
        post_processor: IPostProcessor,
    ) -> typing.Any:
        '''(experimental) Default Token resolution.

        Resolve the Token, recurse into whatever it returns,
        then finally post-process it.

        :param t: -
        :param context: -
        :param post_processor: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DefaultTokenResolver.resolve_token)
            check_type(argname="argument t", value=t, expected_type=type_hints["t"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument post_processor", value=post_processor, expected_type=type_hints["post_processor"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolveToken", [t, context, post_processor]))


class ListTerraformIterator(
    TerraformIterator,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.ListTerraformIterator",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        list: typing.Union[typing.Sequence[builtins.str], IResolvable, typing.Sequence[jsii.Number], ComplexList, StringMapList, NumberMapList, BooleanMapList, AnyMapList, typing.Sequence[typing.Union[builtins.bool, IResolvable]]],
    ) -> None:
        '''
        :param list: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ListTerraformIterator.__init__)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        jsii.create(self.__class__, self, [list])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Any:
        '''(experimental) Returns the currenty entry in the list or set that is being iterated over.

        For lists this is the same as ``iterator.value``. If you need the index,
        use count using the escape hatch:
        https://www.terraform.io/cdktf/concepts/resources#escape-hatch

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) Returns the value of the current item iterated over.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))


class MapTerraformIterator(
    TerraformIterator,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.MapTerraformIterator",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        map: typing.Union[StringMap, NumberMap, BooleanMap, AnyMap, ComplexMap, typing.Mapping[builtins.str, typing.Any], typing.Mapping[builtins.str, builtins.str], typing.Mapping[builtins.str, jsii.Number]],
    ) -> None:
        '''
        :param map: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MapTerraformIterator.__init__)
            check_type(argname="argument map", value=map, expected_type=type_hints["map"])
        jsii.create(self.__class__, self, [map])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        '''(experimental) Returns the key of the current entry in the map that is being iterated over.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) Returns the value of the current item iterated over.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))


class TerraformBackend(
    TerraformElement,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        jsii.create(self.__class__, self, [scope, id, name])

    @jsii.member(jsii_name="isBackend")
    @builtins.classmethod
    def is_backend(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformBackend.is_backend)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isBackend", [x]))

    @jsii.member(jsii_name="getRemoteStateDataSource")
    @abc.abstractmethod
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param from_stack: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''(experimental) Adds this resource to the terraform JSON output.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def _name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class _TerraformBackendProxy(TerraformBackend):
    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument from_stack", value=from_stack, expected_type=type_hints["from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, from_stack]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TerraformBackend).__jsii_proxy_class__ = lambda : _TerraformBackendProxy


@jsii.implements(ITerraformResource, ITerraformDependable, IInterpolatingParent)
class TerraformDataSource(
    TerraformElement,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformDataSource",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        terraform_resource_type: builtins.str,
        terraform_generator_metadata: typing.Optional[typing.Union[TerraformProviderGeneratorMetadata, typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TerraformResourceConfig(
            terraform_resource_type=terraform_resource_type,
            terraform_generator_metadata=terraform_generator_metadata,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="getAnyMapAttribute")
    def get_any_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_any_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "getAnyMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: builtins.str) -> IResolvable:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_boolean_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "getBooleanAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getBooleanMapAttribute")
    def get_boolean_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.bool]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_boolean_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.bool], jsii.invoke(self, "getBooleanMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.List[builtins.str]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_list_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getListAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: builtins.str) -> jsii.Number:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_number_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getNumberAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberListAttribute")
    def get_number_list_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.List[jsii.Number]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_number_list_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.List[jsii.Number], jsii.invoke(self, "getNumberListAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getNumberMapAttribute")
    def get_number_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, jsii.Number]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_number_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.invoke(self, "getNumberMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: builtins.str) -> builtins.str:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_string_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(builtins.str, jsii.invoke(self, "getStringAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="getStringMapAttribute")
    def get_string_map_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.get_string_map_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "getStringMapAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(
        self,
        terraform_attribute: builtins.str,
    ) -> IResolvable:
        '''
        :param terraform_attribute: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformDataSource.interpolation_for_attribute)
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        return typing.cast(IResolvable, jsii.invoke(self, "interpolationForAttribute", [terraform_attribute]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="toMetadata")
    def to_metadata(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toMetadata", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''(experimental) Adds this resource to the terraform JSON output.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))

    @builtins.property
    @jsii.member(jsii_name="terraformMetaArguments")
    def terraform_meta_arguments(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "terraformMetaArguments"))

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "terraformResourceType"))

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional[TerraformProviderGeneratorMetadata]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[TerraformProviderGeneratorMetadata], jsii.get(self, "terraformGeneratorMetadata"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "count"))

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformDataSource, "count").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformDataSource, "depends_on").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="forEach")
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[ITerraformIterator], jsii.get(self, "forEach"))

    @for_each.setter
    def for_each(self, value: typing.Optional[ITerraformIterator]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformDataSource, "for_each").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forEach", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional[TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[TerraformResourceLifecycle], jsii.get(self, "lifecycle"))

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional[TerraformResourceLifecycle]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformDataSource, "lifecycle").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional[TerraformProvider]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[TerraformProvider], jsii.get(self, "provider"))

    @provider.setter
    def provider(self, value: typing.Optional[TerraformProvider]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(TerraformDataSource, "provider").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provider", value)


class TerraformHclModule(
    TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.TerraformHclModule",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        source: builtins.str,
        version: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[TerraformProvider, typing.Union[TerraformModuleProvider, typing.Dict[str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param variables: 
        :param source: 
        :param version: 
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformHclModule.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = TerraformHclModuleOptions(
            variables=variables,
            source=source,
            version=version,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, options])

    @jsii.member(jsii_name="get")
    def get(self, output: builtins.str) -> typing.Any:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformHclModule.get)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(typing.Any, jsii.invoke(self, "get", [output]))

    @jsii.member(jsii_name="getBoolean")
    def get_boolean(self, output: builtins.str) -> IResolvable:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformHclModule.get_boolean)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(IResolvable, jsii.invoke(self, "getBoolean", [output]))

    @jsii.member(jsii_name="getList")
    def get_list(self, output: builtins.str) -> typing.List[builtins.str]:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformHclModule.get_list)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getList", [output]))

    @jsii.member(jsii_name="getNumber")
    def get_number(self, output: builtins.str) -> jsii.Number:
        '''
        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformHclModule.get_number)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getNumber", [output]))

    @jsii.member(jsii_name="set")
    def set(self, variable: builtins.str, value: typing.Any) -> None:
        '''
        :param variable: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformHclModule.set)
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "set", [variable, value]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "variables"))


@jsii.data_type(
    jsii_type="cdktf.TerraformModuleOptions",
    jsii_struct_bases=[TerraformModuleUserOptions],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "source": "source",
        "version": "version",
    },
)
class TerraformModuleOptions(TerraformModuleUserOptions):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[TerraformProvider, typing.Union[TerraformModuleProvider, typing.Dict[str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        source: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param source: 
        :param version: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformModuleOptions.__init__)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {
            "source": source,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[TerraformProvider, TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[TerraformProvider, TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformModuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactoryBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.ArtifactoryBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        password: builtins.str,
        repo: builtins.str,
        subpath: builtins.str,
        url: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param password: (experimental) (Required) - The password.
        :param repo: (experimental) (Required) - The repository name.
        :param subpath: (experimental) (Required) - Path within the repository.
        :param url: (experimental) (Required) - The URL. Note that this is the base url to artifactory not the full repo and subpath.
        :param username: (experimental) (Required) - The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ArtifactoryBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = ArtifactoryBackendProps(
            password=password, repo=repo, subpath=subpath, url=url, username=username
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ArtifactoryBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class AzurermBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.AzurermBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        container_name: builtins.str,
        key: builtins.str,
        storage_account_name: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        msi_endpoint: typing.Optional[builtins.str] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        sas_token: typing.Optional[builtins.str] = None,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_msi: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param container_name: (experimental) (Required) The Name of the Storage Container within the Storage Account.
        :param key: (experimental) (Required) The name of the Blob used to retrieve/store Terraform's State file inside the Storage Container.
        :param storage_account_name: (experimental) (Required) The Name of the Storage Account.
        :param access_key: (experimental) access_key - (Optional) The Access Key used to access the Blob Storage Account. This can also be sourced from the ARM_ACCESS_KEY environment variable.
        :param client_id: (experimental) (Optional) The Client ID of the Service Principal. This can also be sourced from the ARM_CLIENT_ID environment variable.
        :param client_secret: (experimental) (Optional) The Client Secret of the Service Principal. This can also be sourced from the ARM_CLIENT_SECRET environment variable.
        :param endpoint: (experimental) (Optional) The Custom Endpoint for Azure Resource Manager. This can also be sourced from the ARM_ENDPOINT environment variable. NOTE: An endpoint should only be configured when using Azure Stack.
        :param environment: (experimental) (Optional) The Azure Environment which should be used. This can also be sourced from the ARM_ENVIRONMENT environment variable. Possible values are public, china, german, stack and usgovernment. Defaults to public.
        :param msi_endpoint: (experimental) (Optional) The path to a custom Managed Service Identity endpoint which is automatically determined if not specified. This can also be sourced from the ARM_MSI_ENDPOINT environment variable.
        :param resource_group_name: (experimental) (Required) The Name of the Resource Group in which the Storage Account exists.
        :param sas_token: (experimental) (Optional) The SAS Token used to access the Blob Storage Account. This can also be sourced from the ARM_SAS_TOKEN environment variable.
        :param subscription_id: (experimental) (Optional) The Subscription ID in which the Storage Account exists. This can also be sourced from the ARM_SUBSCRIPTION_ID environment variable.
        :param tenant_id: (experimental) (Optional) The Tenant ID in which the Subscription exists. This can also be sourced from the ARM_TENANT_ID environment variable.
        :param use_msi: (experimental) (Optional) Should Managed Service Identity authentication be used? This can also be sourced from the ARM_USE_MSI environment variable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AzurermBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = AzurermBackendProps(
            container_name=container_name,
            key=key,
            storage_account_name=storage_account_name,
            access_key=access_key,
            client_id=client_id,
            client_secret=client_secret,
            endpoint=endpoint,
            environment=environment,
            msi_endpoint=msi_endpoint,
            resource_group_name=resource_group_name,
            sas_token=sas_token,
            subscription_id=subscription_id,
            tenant_id=tenant_id,
            use_msi=use_msi,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AzurermBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class CloudBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.CloudBackend",
):
    '''(experimental) The Cloud Backend synthesizes a {@link https://www.terraform.io/cli/cloud/settings#the-cloud-block cloud block}. The cloud block is a nested block within the top-level terraform settings block. It specifies which Terraform Cloud workspaces to use for the current working directory. The cloud block only affects Terraform CLI's behavior. When Terraform Cloud uses a configuration that contains a cloud block - for example, when a workspace is configured to use a VCS provider directly - it ignores the block and behaves according to its own workspace settings.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        organization: builtins.str,
        workspaces: typing.Union[NamedCloudWorkspace, TaggedCloudWorkspaces],
        hostname: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param organization: (experimental) The name of the organization containing the workspace(s) the current configuration should use.
        :param workspaces: (experimental) A nested block that specifies which remote Terraform Cloud workspaces to use for the current configuration. The workspaces block must contain exactly one of the following arguments, each denoting a strategy for how workspaces should be mapped:
        :param hostname: (experimental) The hostname of a Terraform Enterprise installation, if using Terraform Enterprise. Default: app.terraform.io
        :param token: (experimental) The token used to authenticate with Terraform Cloud. We recommend omitting the token from the configuration, and instead using terraform login or manually configuring credentials in the CLI config file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = CloudBackendProps(
            organization=organization,
            workspaces=workspaces,
            hostname=hostname,
            token=token,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        '''(experimental) Adds this resource to the terraform JSON output.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))


class ConsulBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.ConsulBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        access_token: builtins.str,
        path: builtins.str,
        address: typing.Optional[builtins.str] = None,
        ca_file: typing.Optional[builtins.str] = None,
        cert_file: typing.Optional[builtins.str] = None,
        datacenter: typing.Optional[builtins.str] = None,
        gzip: typing.Optional[builtins.bool] = None,
        http_auth: typing.Optional[builtins.str] = None,
        key_file: typing.Optional[builtins.str] = None,
        lock: typing.Optional[builtins.bool] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param access_token: (experimental) (Required) Access token.
        :param path: (experimental) (Required) Path in the Consul KV store.
        :param address: (experimental) (Optional) DNS name and port of your Consul endpoint specified in the format dnsname:port. Defaults to the local agent HTTP listener.
        :param ca_file: (experimental) (Optional) A path to a PEM-encoded certificate authority used to verify the remote agent's certificate.
        :param cert_file: (experimental) (Optional) A path to a PEM-encoded certificate provided to the remote agent; requires use of key_file.
        :param datacenter: (experimental) (Optional) The datacenter to use. Defaults to that of the agent.
        :param gzip: (experimental) (Optional) true to compress the state data using gzip, or false (the default) to leave it uncompressed.
        :param http_auth: (experimental) (Optional) HTTP Basic Authentication credentials to be used when communicating with Consul, in the format of either user or user:pass.
        :param key_file: (experimental) (Optional) A path to a PEM-encoded private key, required if cert_file is specified.
        :param lock: (experimental) (Optional) false to disable locking. This defaults to true, but will require session permissions with Consul and at least kv write permissions on $path/.lock to perform locking.
        :param scheme: (experimental) (Optional) Specifies what protocol to use when talking to the given address,either http or https. SSL support can also be triggered by setting then environment variable CONSUL_HTTP_SSL to true.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ConsulBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = ConsulBackendProps(
            access_token=access_token,
            path=path,
            address=address,
            ca_file=ca_file,
            cert_file=cert_file,
            datacenter=datacenter,
            gzip=gzip,
            http_auth=http_auth,
            key_file=key_file,
            lock=lock,
            scheme=scheme,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ConsulBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class CosBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.CosBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        bucket: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_id: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param bucket: (experimental) (Required) The name of the COS bucket. You shall manually create it first.
        :param acl: (experimental) (Optional) Object ACL to be applied to the state file, allows private and public-read. Defaults to private.
        :param encrypt: (experimental) (Optional) Whether to enable server side encryption of the state file. If it is true, COS will use 'AES256' encryption algorithm to encrypt state file.
        :param key: (experimental) (Optional) The path for saving the state file in bucket. Defaults to terraform.tfstate.
        :param prefix: (experimental) (Optional) The directory for saving the state file in bucket. Default to "env:".
        :param region: (experimental) (Optional) The region of the COS bucket. It supports environment variables TENCENTCLOUD_REGION.
        :param secret_id: (experimental) (Optional) Secret id of Tencent Cloud. It supports environment variables TENCENTCLOUD_SECRET_ID.
        :param secret_key: (experimental) (Optional) Secret key of Tencent Cloud. It supports environment variables TENCENTCLOUD_SECRET_KEY.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CosBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = CosBackendProps(
            bucket=bucket,
            acl=acl,
            encrypt=encrypt,
            key=key,
            prefix=prefix,
            region=region,
            secret_id=secret_id,
            secret_key=secret_key,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CosBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class EtcdBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.EtcdBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        endpoints: builtins.str,
        path: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param endpoints: (experimental) (Required) A space-separated list of the etcd endpoints.
        :param path: (experimental) (Required) The path where to store the state.
        :param password: (experimental) (Optional) The password.
        :param username: (experimental) (Optional) The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EtcdBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = EtcdBackendProps(
            endpoints=endpoints, path=path, password=password, username=username
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EtcdBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class EtcdV3Backend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.EtcdV3Backend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        endpoints: typing.Sequence[builtins.str],
        cacert_path: typing.Optional[builtins.str] = None,
        cert_path: typing.Optional[builtins.str] = None,
        key_path: typing.Optional[builtins.str] = None,
        lock: typing.Optional[builtins.bool] = None,
        password: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param endpoints: (experimental) (Required) The list of 'etcd' endpoints which to connect to.
        :param cacert_path: (experimental) (Optional) The path to a PEM-encoded CA bundle with which to verify certificates of TLS-enabled etcd servers.
        :param cert_path: (experimental) (Optional) The path to a PEM-encoded certificate to provide to etcd for secure client identification.
        :param key_path: (experimental) (Optional) The path to a PEM-encoded key to provide to etcd for secure client identification.
        :param lock: (experimental) (Optional) Whether to lock state access. Defaults to true.
        :param password: (experimental) (Optional) Password used to connect to the etcd cluster.
        :param prefix: (experimental) (Optional) An optional prefix to be added to keys when to storing state in etcd. Defaults to "".
        :param username: (experimental) (Optional) Username used to connect to the etcd cluster.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EtcdV3Backend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = EtcdV3BackendProps(
            endpoints=endpoints,
            cacert_path=cacert_path,
            cert_path=cert_path,
            key_path=key_path,
            lock=lock,
            password=password,
            prefix=prefix,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EtcdV3Backend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class GcsBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.GcsBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        bucket: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        impersonate_service_account: typing.Optional[builtins.str] = None,
        impersonate_service_account_delegates: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param bucket: (experimental) (Required) The name of the GCS bucket. This name must be globally unique.
        :param access_token: (experimental) (Optional) A temporary [OAuth 2.0 access token] obtained from the Google Authorization server, i.e. the Authorization: Bearer token used to authenticate HTTP requests to GCP APIs. This is an alternative to credentials. If both are specified, access_token will be used over the credentials field.
        :param credentials: (experimental) (Optional) Local path to Google Cloud Platform account credentials in JSON format. If unset, Google Application Default Credentials are used. The provided credentials must have Storage Object Admin role on the bucket. Warning: if using the Google Cloud Platform provider as well, it will also pick up the GOOGLE_CREDENTIALS environment variable.
        :param encryption_key: (experimental) (Optional) A 32 byte base64 encoded 'customer supplied encryption key' used to encrypt all state.
        :param impersonate_service_account: (experimental) (Optional) The service account to impersonate for accessing the State Bucket. You must have roles/iam.serviceAccountTokenCreator role on that account for the impersonation to succeed. If you are using a delegation chain, you can specify that using the impersonate_service_account_delegates field. Alternatively, this can be specified using the GOOGLE_IMPERSONATE_SERVICE_ACCOUNT environment variable.
        :param impersonate_service_account_delegates: (experimental) (Optional) The delegation chain for an impersonating a service account.
        :param prefix: (experimental) (Optional) GCS prefix inside the bucket. Named states for workspaces are stored in an object called /.tfstate.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GcsBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = GcsBackendProps(
            bucket=bucket,
            access_token=access_token,
            credentials=credentials,
            encryption_key=encryption_key,
            impersonate_service_account=impersonate_service_account,
            impersonate_service_account_delegates=impersonate_service_account_delegates,
            prefix=prefix,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GcsBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class HttpBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.HttpBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        address: builtins.str,
        lock_address: typing.Optional[builtins.str] = None,
        lock_method: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        retry_max: typing.Optional[jsii.Number] = None,
        retry_wait_max: typing.Optional[jsii.Number] = None,
        retry_wait_min: typing.Optional[jsii.Number] = None,
        skip_cert_verification: typing.Optional[builtins.bool] = None,
        unlock_address: typing.Optional[builtins.str] = None,
        unlock_method: typing.Optional[builtins.str] = None,
        update_method: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param address: (experimental) (Required) The address of the REST endpoint.
        :param lock_address: (experimental) (Optional) The address of the lock REST endpoint. Defaults to disabled.
        :param lock_method: (experimental) (Optional) The HTTP method to use when locking. Defaults to LOCK.
        :param password: (experimental) (Optional) The password for HTTP basic authentication.
        :param retry_max: (experimental) (Optional) The number of HTTP request retries. Defaults to 2.
        :param retry_wait_max: (experimental) (Optional) The maximum time in seconds to wait between HTTP request attempts. Defaults to 30.
        :param retry_wait_min: (experimental) (Optional) The minimum time in seconds to wait between HTTP request attempts. Defaults to 1.
        :param skip_cert_verification: (experimental) (Optional) Whether to skip TLS verification. Defaults to false.
        :param unlock_address: (experimental) (Optional) The address of the unlock REST endpoint. Defaults to disabled.
        :param unlock_method: (experimental) (Optional) The HTTP method to use when unlocking. Defaults to UNLOCK.
        :param update_method: (experimental) (Optional) HTTP method to use when updating state. Defaults to POST.
        :param username: (experimental) (Optional) The username for HTTP basic authentication.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = HttpBackendProps(
            address=address,
            lock_address=lock_address,
            lock_method=lock_method,
            password=password,
            retry_max=retry_max,
            retry_wait_max=retry_wait_max,
            retry_wait_min=retry_wait_min,
            skip_cert_verification=skip_cert_verification,
            unlock_address=unlock_address,
            unlock_method=unlock_method,
            update_method=update_method,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class LocalBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.LocalBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        path: typing.Optional[builtins.str] = None,
        workspace_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param path: (experimental) Path where the state file is stored. Default: - defaults to terraform.${stackId}.tfstate
        :param workspace_dir: (experimental) (Optional) The path to non-default workspaces.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LocalBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = LocalBackendProps(path=path, workspace_dir=workspace_dir)

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LocalBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument from_stack", value=from_stack, expected_type=type_hints["from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class MantaBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.MantaBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        account: builtins.str,
        key_id: builtins.str,
        path: builtins.str,
        insecure_skip_tls_verify: typing.Optional[builtins.bool] = None,
        key_material: typing.Optional[builtins.str] = None,
        object_name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param account: 
        :param key_id: 
        :param path: 
        :param insecure_skip_tls_verify: 
        :param key_material: 
        :param object_name: 
        :param url: 
        :param user: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MantaBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = MantaBackendProps(
            account=account,
            key_id=key_id,
            path=path,
            insecure_skip_tls_verify=insecure_skip_tls_verify,
            key_material=key_material,
            object_name=object_name,
            url=url,
            user=user,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MantaBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class OssBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.OssBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        bucket: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        assume_role: typing.Optional[typing.Union[OssAssumeRole, typing.Dict[str, typing.Any]]] = None,
        ecs_role_name: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        security_token: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        tablestore_endpoint: typing.Optional[builtins.str] = None,
        tablestore_table: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param bucket: 
        :param access_key: 
        :param acl: 
        :param assume_role: 
        :param ecs_role_name: 
        :param encrypt: 
        :param endpoint: 
        :param key: 
        :param prefix: 
        :param profile: 
        :param region: 
        :param secret_key: 
        :param security_token: 
        :param shared_credentials_file: 
        :param tablestore_endpoint: 
        :param tablestore_table: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OssBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = OssBackendProps(
            bucket=bucket,
            access_key=access_key,
            acl=acl,
            assume_role=assume_role,
            ecs_role_name=ecs_role_name,
            encrypt=encrypt,
            endpoint=endpoint,
            key=key,
            prefix=prefix,
            profile=profile,
            region=region,
            secret_key=secret_key,
            security_token=security_token,
            shared_credentials_file=shared_credentials_file,
            tablestore_endpoint=tablestore_endpoint,
            tablestore_table=tablestore_table,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OssBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class PgBackend(TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.PgBackend"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        conn_str: builtins.str,
        schema_name: typing.Optional[builtins.str] = None,
        skip_schema_creation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param conn_str: 
        :param schema_name: 
        :param skip_schema_creation: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PgBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = PgBackendProps(
            conn_str=conn_str,
            schema_name=schema_name,
            skip_schema_creation=skip_schema_creation,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PgBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class RemoteBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.RemoteBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        organization: builtins.str,
        workspaces: IRemoteWorkspace,
        hostname: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = RemoteBackendProps(
            organization=organization,
            workspaces=workspaces,
            hostname=hostname,
            token=token,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class S3Backend(TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.S3Backend"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        bucket: builtins.str,
        key: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        acl: typing.Optional[builtins.str] = None,
        assume_role_policy: typing.Optional[builtins.str] = None,
        assume_role_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        assume_role_transitive_tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        dynamodb_endpoint: typing.Optional[builtins.str] = None,
        dynamodb_table: typing.Optional[builtins.str] = None,
        encrypt: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        force_path_style: typing.Optional[builtins.bool] = None,
        iam_endpoint: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        session_name: typing.Optional[builtins.str] = None,
        shared_credentials_file: typing.Optional[builtins.str] = None,
        skip_credentials_validation: typing.Optional[builtins.bool] = None,
        skip_metadata_api_check: typing.Optional[builtins.bool] = None,
        skip_region_validation: typing.Optional[builtins.bool] = None,
        sse_customer_key: typing.Optional[builtins.str] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        workspace_key_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param bucket: (experimental) Name of the S3 Bucket.
        :param key: (experimental) Path to the state file inside the S3 Bucket. When using a non-default workspace, the state path will be /workspace_key_prefix/workspace_name/key
        :param access_key: (experimental) (Optional) AWS access key. If configured, must also configure secret_key. This can also be sourced from the AWS_ACCESS_KEY_ID environment variable, AWS shared credentials file (e.g. ~/.aws/credentials), or AWS shared configuration file (e.g. ~/.aws/config).
        :param acl: (experimental) (Optional) Canned ACL to be applied to the state file.
        :param assume_role_policy: (experimental) (Optional) IAM Policy JSON describing further restricting permissions for the IAM Role being assumed.
        :param assume_role_policy_arns: (experimental) (Optional) Set of Amazon Resource Names (ARNs) of IAM Policies describing further restricting permissions for the IAM Role being assumed.
        :param assume_role_tags: (experimental) (Optional) Map of assume role session tags.
        :param assume_role_transitive_tag_keys: (experimental) (Optional) Set of assume role session tag keys to pass to any subsequent sessions.
        :param dynamodb_endpoint: (experimental) (Optional) Custom endpoint for the AWS DynamoDB API. This can also be sourced from the AWS_DYNAMODB_ENDPOINT environment variable.
        :param dynamodb_table: (experimental) (Optional) Name of DynamoDB Table to use for state locking and consistency. The table must have a partition key named LockID with type of String. If not configured, state locking will be disabled.
        :param encrypt: (experimental) (Optional) Enable server side encryption of the state file.
        :param endpoint: (experimental) (Optional) Custom endpoint for the AWS S3 API. This can also be sourced from the AWS_S3_ENDPOINT environment variable.
        :param external_id: (experimental) (Optional) External identifier to use when assuming the role.
        :param force_path_style: (experimental) (Optional) Enable path-style S3 URLs (https:/// instead of https://.).
        :param iam_endpoint: (experimental) (Optional) Custom endpoint for the AWS Identity and Access Management (IAM) API. This can also be sourced from the AWS_IAM_ENDPOINT environment variable.
        :param kms_key_id: (experimental) (Optional) Amazon Resource Name (ARN) of a Key Management Service (KMS) Key to use for encrypting the state. Note that if this value is specified, Terraform will need kms:Encrypt, kms:Decrypt and kms:GenerateDataKey permissions on this KMS key.
        :param max_retries: (experimental) (Optional) The maximum number of times an AWS API request is retried on retryable failure. Defaults to 5.
        :param profile: (experimental) (Optional) Name of AWS profile in AWS shared credentials file (e.g. ~/.aws/credentials) or AWS shared configuration file (e.g. ~/.aws/config) to use for credentials and/or configuration. This can also be sourced from the AWS_PROFILE environment variable.
        :param region: (experimental) AWS Region of the S3 Bucket and DynamoDB Table (if used). This can also be sourced from the AWS_DEFAULT_REGION and AWS_REGION environment variables.
        :param role_arn: (experimental) (Optional) Amazon Resource Name (ARN) of the IAM Role to assume.
        :param secret_key: (experimental) (Optional) AWS secret access key. If configured, must also configure access_key. This can also be sourced from the AWS_SECRET_ACCESS_KEY environment variable, AWS shared credentials file (e.g. ~/.aws/credentials), or AWS shared configuration file (e.g. ~/.aws/config)
        :param session_name: (experimental) (Optional) Session name to use when assuming the role.
        :param shared_credentials_file: (experimental) (Optional) Path to the AWS shared credentials file. Defaults to ~/.aws/credentials.
        :param skip_credentials_validation: (experimental) (Optional) Skip credentials validation via the STS API.
        :param skip_metadata_api_check: (experimental) (Optional) Skip usage of EC2 Metadata API.
        :param skip_region_validation: (experimental) (Optional) Skip validation of provided region name.
        :param sse_customer_key: (experimental) (Optional) The key to use for encrypting state with Server-Side Encryption with Customer-Provided Keys (SSE-C). This is the base64-encoded value of the key, which must decode to 256 bits. This can also be sourced from the AWS_SSE_CUSTOMER_KEY environment variable, which is recommended due to the sensitivity of the value. Setting it inside a terraform file will cause it to be persisted to disk in terraform.tfstate.
        :param sts_endpoint: (experimental) (Optional) Custom endpoint for the AWS Security Token Service (STS) API. This can also be sourced from the AWS_STS_ENDPOINT environment variable.
        :param token: (experimental) (Optional) Multi-Factor Authentication (MFA) token. This can also be sourced from the AWS_SESSION_TOKEN environment variable.
        :param workspace_key_prefix: (experimental) (Optional) Prefix applied to the state path inside the bucket. This is only relevant when using a non-default workspace. Defaults to env:

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Backend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = S3BackendProps(
            bucket=bucket,
            key=key,
            access_key=access_key,
            acl=acl,
            assume_role_policy=assume_role_policy,
            assume_role_policy_arns=assume_role_policy_arns,
            assume_role_tags=assume_role_tags,
            assume_role_transitive_tag_keys=assume_role_transitive_tag_keys,
            dynamodb_endpoint=dynamodb_endpoint,
            dynamodb_table=dynamodb_table,
            encrypt=encrypt,
            endpoint=endpoint,
            external_id=external_id,
            force_path_style=force_path_style,
            iam_endpoint=iam_endpoint,
            kms_key_id=kms_key_id,
            max_retries=max_retries,
            profile=profile,
            region=region,
            role_arn=role_arn,
            secret_key=secret_key,
            session_name=session_name,
            shared_credentials_file=shared_credentials_file,
            skip_credentials_validation=skip_credentials_validation,
            skip_metadata_api_check=skip_metadata_api_check,
            skip_region_validation=skip_region_validation,
            sse_customer_key=sse_customer_key,
            sts_endpoint=sts_endpoint,
            token=token,
            workspace_key_prefix=workspace_key_prefix,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Backend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


class SwiftBackend(
    TerraformBackend,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.SwiftBackend",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        container: builtins.str,
        application_credential_id: typing.Optional[builtins.str] = None,
        application_credential_name: typing.Optional[builtins.str] = None,
        application_credential_secret: typing.Optional[builtins.str] = None,
        archive_container: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        default_domain: typing.Optional[builtins.str] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        expire_after: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        project_domain_id: typing.Optional[builtins.str] = None,
        project_domain_name: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        state_name: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_domain_id: typing.Optional[builtins.str] = None,
        user_domain_name: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param container: 
        :param application_credential_id: 
        :param application_credential_name: 
        :param application_credential_secret: 
        :param archive_container: 
        :param auth_url: 
        :param cacert_file: 
        :param cert: 
        :param cloud: 
        :param default_domain: 
        :param domain_id: 
        :param domain_name: 
        :param expire_after: 
        :param insecure: 
        :param key: 
        :param password: 
        :param project_domain_id: 
        :param project_domain_name: 
        :param region_name: 
        :param state_name: 
        :param tenant_id: 
        :param tenant_name: 
        :param token: 
        :param user_domain_id: 
        :param user_domain_name: 
        :param user_id: 
        :param user_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SwiftBackend.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = SwiftBackendProps(
            container=container,
            application_credential_id=application_credential_id,
            application_credential_name=application_credential_name,
            application_credential_secret=application_credential_secret,
            archive_container=archive_container,
            auth_url=auth_url,
            cacert_file=cacert_file,
            cert=cert,
            cloud=cloud,
            default_domain=default_domain,
            domain_id=domain_id,
            domain_name=domain_name,
            expire_after=expire_after,
            insecure=insecure,
            key=key,
            password=password,
            project_domain_id=project_domain_id,
            project_domain_name=project_domain_name,
            region_name=region_name,
            state_name=state_name,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            token=token,
            user_domain_id=user_domain_id,
            user_domain_name=user_domain_name,
            user_id=user_id,
            user_name=user_name,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="getRemoteStateDataSource")
    def get_remote_state_data_source(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        _from_stack: builtins.str,
    ) -> TerraformRemoteState:
        '''(experimental) Creates a TerraformRemoteState resource that accesses this backend.

        :param scope: -
        :param name: -
        :param _from_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SwiftBackend.get_remote_state_data_source)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument _from_stack", value=_from_stack, expected_type=type_hints["_from_stack"])
        return typing.cast(TerraformRemoteState, jsii.invoke(self, "getRemoteStateDataSource", [scope, name, _from_stack]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))


@jsii.data_type(
    jsii_type="cdktf.TerraformHclModuleOptions",
    jsii_struct_bases=[TerraformModuleOptions],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "source": "source",
        "version": "version",
        "variables": "variables",
    },
)
class TerraformHclModuleOptions(TerraformModuleOptions):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[ITerraformDependable]] = None,
        for_each: typing.Optional[ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[TerraformProvider, typing.Union[TerraformModuleProvider, typing.Dict[str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        source: builtins.str,
        version: typing.Optional[builtins.str] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param source: 
        :param version: 
        :param variables: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TerraformHclModuleOptions.__init__)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[str, typing.Any] = {
            "source": source,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if version is not None:
            self._values["version"] = version
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[TerraformProvider, TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[TerraformProvider, TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformHclModuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AnnotationMetadataEntryType",
    "Annotations",
    "AnyMap",
    "AnyMapList",
    "App",
    "AppOptions",
    "ArtifactoryBackend",
    "ArtifactoryBackendProps",
    "Aspects",
    "AssetType",
    "AzurermBackend",
    "AzurermBackendProps",
    "BooleanMap",
    "BooleanMapList",
    "CloudBackend",
    "CloudBackendProps",
    "CloudWorkspace",
    "ComplexComputedList",
    "ComplexList",
    "ComplexMap",
    "ComplexObject",
    "ConsulBackend",
    "ConsulBackendProps",
    "CosBackend",
    "CosBackendProps",
    "DataTerraformRemoteState",
    "DataTerraformRemoteStateArtifactory",
    "DataTerraformRemoteStateArtifactoryConfig",
    "DataTerraformRemoteStateAzurerm",
    "DataTerraformRemoteStateAzurermConfig",
    "DataTerraformRemoteStateConfig",
    "DataTerraformRemoteStateConsul",
    "DataTerraformRemoteStateConsulConfig",
    "DataTerraformRemoteStateCos",
    "DataTerraformRemoteStateCosConfig",
    "DataTerraformRemoteStateEtcd",
    "DataTerraformRemoteStateEtcdConfig",
    "DataTerraformRemoteStateEtcdV3",
    "DataTerraformRemoteStateEtcdV3Config",
    "DataTerraformRemoteStateGcs",
    "DataTerraformRemoteStateGcsConfig",
    "DataTerraformRemoteStateHttp",
    "DataTerraformRemoteStateHttpConfig",
    "DataTerraformRemoteStateLocal",
    "DataTerraformRemoteStateLocalConfig",
    "DataTerraformRemoteStateManta",
    "DataTerraformRemoteStateMantaConfig",
    "DataTerraformRemoteStateOss",
    "DataTerraformRemoteStateOssConfig",
    "DataTerraformRemoteStatePg",
    "DataTerraformRemoteStatePgConfig",
    "DataTerraformRemoteStateRemoteConfig",
    "DataTerraformRemoteStateS3",
    "DataTerraformRemoteStateS3Config",
    "DataTerraformRemoteStateSwift",
    "DataTerraformRemoteStateSwiftConfig",
    "DefaultTokenResolver",
    "EncodingOptions",
    "EtcdBackend",
    "EtcdBackendProps",
    "EtcdV3Backend",
    "EtcdV3BackendProps",
    "FileProvisioner",
    "Fn",
    "GcsBackend",
    "GcsBackendProps",
    "HttpBackend",
    "HttpBackendProps",
    "IAnyProducer",
    "IAspect",
    "IFragmentConcatenator",
    "IInterpolatingParent",
    "IListProducer",
    "IManifest",
    "INumberProducer",
    "IPostProcessor",
    "IRemoteWorkspace",
    "IResolvable",
    "IResolveContext",
    "IResource",
    "IResourceConstructor",
    "IScopeCallback",
    "IStackSynthesizer",
    "IStringProducer",
    "ISynthesisSession",
    "ITerraformAddressable",
    "ITerraformDependable",
    "ITerraformIterator",
    "ITerraformResource",
    "ITokenMapper",
    "ITokenResolver",
    "Lazy",
    "LazyAnyValueOptions",
    "LazyBase",
    "LazyListValueOptions",
    "LazyStringValueOptions",
    "ListTerraformIterator",
    "LocalBackend",
    "LocalBackendProps",
    "LocalExecProvisioner",
    "Manifest",
    "MantaBackend",
    "MantaBackendProps",
    "MapTerraformIterator",
    "NamedCloudWorkspace",
    "NamedRemoteWorkspace",
    "NumberMap",
    "NumberMapList",
    "OssAssumeRole",
    "OssBackend",
    "OssBackendProps",
    "PgBackend",
    "PgBackendProps",
    "PrefixedRemoteWorkspaces",
    "RemoteBackend",
    "RemoteBackendProps",
    "RemoteExecProvisioner",
    "ResolveOptions",
    "Resource",
    "S3Backend",
    "S3BackendProps",
    "SSHProvisionerConnection",
    "StackAnnotation",
    "StackManifest",
    "StringConcat",
    "StringMap",
    "StringMapList",
    "SwiftBackend",
    "SwiftBackendProps",
    "TaggedCloudWorkspaces",
    "TerraformAsset",
    "TerraformAssetConfig",
    "TerraformBackend",
    "TerraformDataSource",
    "TerraformElement",
    "TerraformElementMetadata",
    "TerraformHclModule",
    "TerraformHclModuleOptions",
    "TerraformIterator",
    "TerraformLocal",
    "TerraformMetaArguments",
    "TerraformModule",
    "TerraformModuleOptions",
    "TerraformModuleProvider",
    "TerraformModuleUserOptions",
    "TerraformOutput",
    "TerraformOutputConfig",
    "TerraformProvider",
    "TerraformProviderConfig",
    "TerraformProviderGeneratorMetadata",
    "TerraformRemoteState",
    "TerraformResource",
    "TerraformResourceConfig",
    "TerraformResourceLifecycle",
    "TerraformSelf",
    "TerraformStack",
    "TerraformStackMetadata",
    "TerraformVariable",
    "TerraformVariableConfig",
    "TerraformVariableValidationConfig",
    "Testing",
    "TestingAppOptions",
    "Token",
    "Tokenization",
    "TokenizedStringFragments",
    "VariableType",
    "WinrmProvisionerConnection",
    "testing_matchers",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import testing_matchers
