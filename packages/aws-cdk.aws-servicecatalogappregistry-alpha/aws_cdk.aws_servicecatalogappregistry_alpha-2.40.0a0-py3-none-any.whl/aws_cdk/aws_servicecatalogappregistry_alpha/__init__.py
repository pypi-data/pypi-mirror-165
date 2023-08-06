'''
# AWS ServiceCatalogAppRegistry Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[AWS Service Catalog App Registry](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/appregistry.html)
enables organizations to create and manage repositores of applications and associated resources.

## Table Of Contents

* [Application](#application)
* [Attribute-Group](#attribute-group)
* [Associations](#associations)

  * [Associating application with an attribute group](#attribute-group-association)
  * [Associating application with a stack](#resource-association)
* [Sharing](#sharing)

  * [Sharing an application](#sharing-an-application)
  * [Sharing an attribute group](#sharing-an-attribute-group)

The `@aws-cdk/aws-servicecatalogappregistry` package contains resources that enable users to automate governance and management of their AWS resources at scale.

```python
import aws_cdk.aws_servicecatalogappregistry_alpha as appreg
```

## Application

An AppRegistry application enables you to define your applications and associated resources.
The application name must be unique at the account level, but is mutable.

```python
application = appreg.Application(self, "MyFirstApplication",
    application_name="MyFirstApplicationName",
    description="description for my application"
)
```

An application that has been created outside of the stack can be imported into your CDK app.
Applications can be imported by their ARN via the `Application.fromApplicationArn()` API:

```python
imported_application = appreg.Application.from_application_arn(self, "MyImportedApplication", "arn:aws:servicecatalog:us-east-1:012345678910:/applications/0aqmvxvgmry0ecc4mjhwypun6i")
```

## Attribute Group

An AppRegistry attribute group acts as a container for user-defined attributes for an application.
Metadata is attached in a machine-readble format to integrate with automated workflows and tools.

```python
attribute_group = appreg.AttributeGroup(self, "MyFirstAttributeGroup",
    attribute_group_name="MyFirstAttributeGroupName",
    description="description for my attribute group",  # the description is optional,
    attributes={
        "project": "foo",
        "team": ["member1", "member2", "member3"],
        "public": False,
        "stages": {
            "alpha": "complete",
            "beta": "incomplete",
            "release": "not started"
        }
    }
)
```

An attribute group that has been created outside of the stack can be imported into your CDK app.
Attribute groups can be imported by their ARN via the `AttributeGroup.fromAttributeGroupArn()` API:

```python
imported_attribute_group = appreg.AttributeGroup.from_attribute_group_arn(self, "MyImportedAttrGroup", "arn:aws:servicecatalog:us-east-1:012345678910:/attribute-groups/0aqmvxvgmry0ecc4mjhwypun6i")
```

## Associations

You can associate your appregistry application with attribute groups and resources.
Resources are CloudFormation stacks that you can associate with an application to group relevant
stacks together to enable metadata rich insights into your applications and resources.
A Cloudformation stack can only be associated with one appregistry application.
If a stack is associated with multiple applications in your app or is already associated with one,
CDK will fail at deploy time.

### Associating application with an attribute group

You can associate an attribute group with an application with the `associateAttributeGroup()` API:

```python
# application: appreg.Application
# attribute_group: appreg.AttributeGroup

application.associate_attribute_group(attribute_group)
```

### Associating application with a Stack

You can associate a stack with an application with the `associateStack()` API:

```python
# application: appreg.Application
app = App()
my_stack = Stack(app, "MyStack")
application.associate_stack(my_stack)
```

## Sharing

You can share your AppRegistry applications and attribute groups with AWS Organizations, Organizational Units (OUs), AWS accounts within an organization, as well as IAM roles and users. AppRegistry requires that AWS Organizations is enabled in an account before deploying a share of an application or attribute group.

### Sharing an application

```python
import aws_cdk.aws_iam as iam
# application: appreg.Application
# my_role: iam.IRole
# my_user: iam.IUser

application.share_application(
    accounts=["123456789012"],
    organization_arns=["arn:aws:organizations::123456789012:organization/o-my-org-id"],
    roles=[my_role],
    users=[my_user]
)
```

E.g., sharing an application with multiple accounts and allowing the accounts to associate resources to the application.

```python
import aws_cdk.aws_iam as iam
# application: appreg.Application

application.share_application(
    accounts=["123456789012", "234567890123"],
    share_permission=appreg.SharePermission.ALLOW_ACCESS
)
```

### Sharing an attribute group

```python
import aws_cdk.aws_iam as iam
# attribute_group: appreg.AttributeGroup
# my_role: iam.IRole
# my_user: iam.IUser

attribute_group.share_attribute_group(
    accounts=["123456789012"],
    organization_arns=["arn:aws:organizations::123456789012:organization/o-my-org-id"],
    roles=[my_role],
    users=[my_user]
)
```

E.g., sharing an application with multiple accounts and allowing the accounts to associate applications to the attribute group.

```python
import aws_cdk.aws_iam as iam
# attribute_group: appreg.AttributeGroup

attribute_group.share_attribute_group(
    accounts=["123456789012", "234567890123"],
    share_permission=appreg.SharePermission.ALLOW_ACCESS
)
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

import aws_cdk
import aws_cdk.aws_iam
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicecatalogappregistry-alpha.ApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName", "description": "description"},
)
class ApplicationProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a Service Catalog AppRegistry Application.

        :param application_name: (experimental) Enforces a particular physical application name.
        :param description: (experimental) Description for application. Default: - No description provided

        :stability: experimental
        :exampleMetadata: infused

        Example::

            application = appreg.Application(self, "MyFirstApplication",
                application_name="MyFirstApplicationName",
                description="description for my application"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ApplicationProps.__init__)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[str, typing.Any] = {
            "application_name": application_name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def application_name(self) -> builtins.str:
        '''(experimental) Enforces a particular physical application name.

        :stability: experimental
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for application.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicecatalogappregistry-alpha.AttributeGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_group_name": "attributeGroupName",
        "attributes": "attributes",
        "description": "description",
    },
)
class AttributeGroupProps:
    def __init__(
        self,
        *,
        attribute_group_name: builtins.str,
        attributes: typing.Mapping[builtins.str, typing.Any],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a Service Catalog AppRegistry Attribute Group.

        :param attribute_group_name: (experimental) Enforces a particular physical attribute group name.
        :param attributes: (experimental) A JSON of nested key-value pairs that represent the attributes in the group. Attributes maybe an empty JSON '{}', but must be explicitly stated.
        :param description: (experimental) Description for attribute group. Default: - No description provided

        :stability: experimental
        :exampleMetadata: infused

        Example::

            attribute_group = appreg.AttributeGroup(self, "MyFirstAttributeGroup",
                attribute_group_name="MyFirstAttributeGroupName",
                description="description for my attribute group",  # the description is optional,
                attributes={
                    "project": "foo",
                    "team": ["member1", "member2", "member3"],
                    "public": False,
                    "stages": {
                        "alpha": "complete",
                        "beta": "incomplete",
                        "release": "not started"
                    }
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttributeGroupProps.__init__)
            check_type(argname="argument attribute_group_name", value=attribute_group_name, expected_type=type_hints["attribute_group_name"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[str, typing.Any] = {
            "attribute_group_name": attribute_group_name,
            "attributes": attributes,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def attribute_group_name(self) -> builtins.str:
        '''(experimental) Enforces a particular physical attribute group name.

        :stability: experimental
        '''
        result = self._values.get("attribute_group_name")
        assert result is not None, "Required property 'attribute_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) A JSON of nested key-value pairs that represent the attributes in the group.

        Attributes maybe an empty JSON '{}', but must be explicitly stated.

        :stability: experimental
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for attribute group.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttributeGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-servicecatalogappregistry-alpha.IApplication")
class IApplication(aws_cdk.IResource, typing_extensions.Protocol):
    '''(experimental) A Service Catalog AppRegistry Application.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''(experimental) The ID of the application.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="associateAttributeGroup")
    def associate_attribute_group(self, attribute_group: "IAttributeGroup") -> None:
        '''(experimental) Associate thisapplication with an attribute group.

        :param attribute_group: AppRegistry attribute group.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="associateStack")
    def associate_stack(self, stack: aws_cdk.Stack) -> None:
        '''(experimental) Associate this application with a CloudFormation stack.

        :param stack: a CFN stack.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="shareApplication")
    def share_application(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        share_permission: typing.Optional[typing.Union[builtins.str, "SharePermission"]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''(experimental) Share this application with other IAM entities, accounts, or OUs.

        :param accounts: (experimental) A list of AWS accounts that the application will be shared with. Default: - No accounts specified for share
        :param organization_arns: (experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with. Default: - No AWS Organizations or OUs specified for share
        :param roles: (experimental) A list of AWS IAM roles that the application will be shared with. Default: - No IAM roles specified for share
        :param share_permission: (experimental) An option to manage access to the application or attribute group. Default: - Principals will be assigned read only permissions on the application or attribute group.
        :param users: (experimental) A list of AWS IAM users that the application will be shared with. Default: - No IAM Users specified for share

        :stability: experimental
        '''
        ...


class _IApplicationProxy(
    jsii.proxy_for(aws_cdk.IResource), # type: ignore[misc]
):
    '''(experimental) A Service Catalog AppRegistry Application.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-servicecatalogappregistry-alpha.IApplication"

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''(experimental) The ID of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @jsii.member(jsii_name="associateAttributeGroup")
    def associate_attribute_group(self, attribute_group: "IAttributeGroup") -> None:
        '''(experimental) Associate thisapplication with an attribute group.

        :param attribute_group: AppRegistry attribute group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IApplication.associate_attribute_group)
            check_type(argname="argument attribute_group", value=attribute_group, expected_type=type_hints["attribute_group"])
        return typing.cast(None, jsii.invoke(self, "associateAttributeGroup", [attribute_group]))

    @jsii.member(jsii_name="associateStack")
    def associate_stack(self, stack: aws_cdk.Stack) -> None:
        '''(experimental) Associate this application with a CloudFormation stack.

        :param stack: a CFN stack.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IApplication.associate_stack)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "associateStack", [stack]))

    @jsii.member(jsii_name="shareApplication")
    def share_application(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        share_permission: typing.Optional[typing.Union[builtins.str, "SharePermission"]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''(experimental) Share this application with other IAM entities, accounts, or OUs.

        :param accounts: (experimental) A list of AWS accounts that the application will be shared with. Default: - No accounts specified for share
        :param organization_arns: (experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with. Default: - No AWS Organizations or OUs specified for share
        :param roles: (experimental) A list of AWS IAM roles that the application will be shared with. Default: - No IAM roles specified for share
        :param share_permission: (experimental) An option to manage access to the application or attribute group. Default: - Principals will be assigned read only permissions on the application or attribute group.
        :param users: (experimental) A list of AWS IAM users that the application will be shared with. Default: - No IAM Users specified for share

        :stability: experimental
        '''
        share_options = ShareOptions(
            accounts=accounts,
            organization_arns=organization_arns,
            roles=roles,
            share_permission=share_permission,
            users=users,
        )

        return typing.cast(None, jsii.invoke(self, "shareApplication", [share_options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplication).__jsii_proxy_class__ = lambda : _IApplicationProxy


@jsii.interface(
    jsii_type="@aws-cdk/aws-servicecatalogappregistry-alpha.IAttributeGroup"
)
class IAttributeGroup(aws_cdk.IResource, typing_extensions.Protocol):
    '''(experimental) A Service Catalog AppRegistry Attribute Group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="attributeGroupArn")
    def attribute_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the attribute group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="attributeGroupId")
    def attribute_group_id(self) -> builtins.str:
        '''(experimental) The ID of the attribute group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="shareAttributeGroup")
    def share_attribute_group(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        share_permission: typing.Optional[typing.Union[builtins.str, "SharePermission"]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''(experimental) Share the attribute group resource with other IAM entities, accounts, or OUs.

        :param accounts: (experimental) A list of AWS accounts that the application will be shared with. Default: - No accounts specified for share
        :param organization_arns: (experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with. Default: - No AWS Organizations or OUs specified for share
        :param roles: (experimental) A list of AWS IAM roles that the application will be shared with. Default: - No IAM roles specified for share
        :param share_permission: (experimental) An option to manage access to the application or attribute group. Default: - Principals will be assigned read only permissions on the application or attribute group.
        :param users: (experimental) A list of AWS IAM users that the application will be shared with. Default: - No IAM Users specified for share

        :stability: experimental
        '''
        ...


class _IAttributeGroupProxy(
    jsii.proxy_for(aws_cdk.IResource), # type: ignore[misc]
):
    '''(experimental) A Service Catalog AppRegistry Attribute Group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-servicecatalogappregistry-alpha.IAttributeGroup"

    @builtins.property
    @jsii.member(jsii_name="attributeGroupArn")
    def attribute_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the attribute group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="attributeGroupId")
    def attribute_group_id(self) -> builtins.str:
        '''(experimental) The ID of the attribute group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroupId"))

    @jsii.member(jsii_name="shareAttributeGroup")
    def share_attribute_group(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        share_permission: typing.Optional[typing.Union[builtins.str, "SharePermission"]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''(experimental) Share the attribute group resource with other IAM entities, accounts, or OUs.

        :param accounts: (experimental) A list of AWS accounts that the application will be shared with. Default: - No accounts specified for share
        :param organization_arns: (experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with. Default: - No AWS Organizations or OUs specified for share
        :param roles: (experimental) A list of AWS IAM roles that the application will be shared with. Default: - No IAM roles specified for share
        :param share_permission: (experimental) An option to manage access to the application or attribute group. Default: - Principals will be assigned read only permissions on the application or attribute group.
        :param users: (experimental) A list of AWS IAM users that the application will be shared with. Default: - No IAM Users specified for share

        :stability: experimental
        '''
        share_options = ShareOptions(
            accounts=accounts,
            organization_arns=organization_arns,
            roles=roles,
            share_permission=share_permission,
            users=users,
        )

        return typing.cast(None, jsii.invoke(self, "shareAttributeGroup", [share_options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAttributeGroup).__jsii_proxy_class__ = lambda : _IAttributeGroupProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicecatalogappregistry-alpha.ShareOptions",
    jsii_struct_bases=[],
    name_mapping={
        "accounts": "accounts",
        "organization_arns": "organizationArns",
        "roles": "roles",
        "share_permission": "sharePermission",
        "users": "users",
    },
)
class ShareOptions:
    def __init__(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        share_permission: typing.Optional[typing.Union[builtins.str, "SharePermission"]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''(experimental) The options that are passed into a share of an Application or Attribute Group.

        :param accounts: (experimental) A list of AWS accounts that the application will be shared with. Default: - No accounts specified for share
        :param organization_arns: (experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with. Default: - No AWS Organizations or OUs specified for share
        :param roles: (experimental) A list of AWS IAM roles that the application will be shared with. Default: - No IAM roles specified for share
        :param share_permission: (experimental) An option to manage access to the application or attribute group. Default: - Principals will be assigned read only permissions on the application or attribute group.
        :param users: (experimental) A list of AWS IAM users that the application will be shared with. Default: - No IAM Users specified for share

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iam as iam
            # application: appreg.Application
            # my_role: iam.IRole
            # my_user: iam.IUser
            
            application.share_application(
                accounts=["123456789012"],
                organization_arns=["arn:aws:organizations::123456789012:organization/o-my-org-id"],
                roles=[my_role],
                users=[my_user]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ShareOptions.__init__)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument organization_arns", value=organization_arns, expected_type=type_hints["organization_arns"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument share_permission", value=share_permission, expected_type=type_hints["share_permission"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[str, typing.Any] = {}
        if accounts is not None:
            self._values["accounts"] = accounts
        if organization_arns is not None:
            self._values["organization_arns"] = organization_arns
        if roles is not None:
            self._values["roles"] = roles
        if share_permission is not None:
            self._values["share_permission"] = share_permission
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of AWS accounts that the application will be shared with.

        :default: - No accounts specified for share

        :stability: experimental
        '''
        result = self._values.get("accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organization_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with.

        :default: - No AWS Organizations or OUs specified for share

        :stability: experimental
        '''
        result = self._values.get("organization_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.IRole]]:
        '''(experimental) A list of AWS IAM roles that the application will be shared with.

        :default: - No IAM roles specified for share

        :stability: experimental
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IRole]], result)

    @builtins.property
    def share_permission(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "SharePermission"]]:
        '''(experimental) An option to manage access to the application or attribute group.

        :default: - Principals will be assigned read only permissions on the application or attribute group.

        :stability: experimental
        '''
        result = self._values.get("share_permission")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "SharePermission"]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.IUser]]:
        '''(experimental) A list of AWS IAM users that the application will be shared with.

        :default: - No IAM Users specified for share

        :stability: experimental
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IUser]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShareOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-servicecatalogappregistry-alpha.SharePermission")
class SharePermission(enum.Enum):
    '''(experimental) Supported permissions for sharing applications or attribute groups with principals using AWS RAM.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iam as iam
        # application: appreg.Application
        
        application.share_application(
            accounts=["123456789012", "234567890123"],
            share_permission=appreg.SharePermission.ALLOW_ACCESS
        )
    '''

    READ_ONLY = "READ_ONLY"
    '''(experimental) Allows principals in the share to only view the application or attribute group.

    :stability: experimental
    '''
    ALLOW_ACCESS = "ALLOW_ACCESS"
    '''(experimental) Allows principals in the share to associate resources and attribute groups with applications.

    :stability: experimental
    '''


@jsii.implements(IApplication)
class Application(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicecatalogappregistry-alpha.Application",
):
    '''(experimental) A Service Catalog AppRegistry Application.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        application = appreg.Application(self, "MyFirstApplication",
            application_name="MyFirstApplicationName",
            description="description for my application"
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_name: (experimental) Enforces a particular physical application name.
        :param description: (experimental) Description for application. Default: - No description provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Application.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationProps(
            application_name=application_name, description=description
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationArn")
    @builtins.classmethod
    def from_application_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        application_arn: builtins.str,
    ) -> IApplication:
        '''(experimental) Imports an Application construct that represents an external application.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param application_arn: the Amazon Resource Name of the existing AppRegistry Application.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Application.from_application_arn)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
        return typing.cast(IApplication, jsii.sinvoke(cls, "fromApplicationArn", [scope, id, application_arn]))

    @jsii.member(jsii_name="associateAttributeGroup")
    def associate_attribute_group(self, attribute_group: IAttributeGroup) -> None:
        '''(experimental) Associate an attribute group with application If the attribute group is already associated, it will ignore duplicate request.

        :param attribute_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Application.associate_attribute_group)
            check_type(argname="argument attribute_group", value=attribute_group, expected_type=type_hints["attribute_group"])
        return typing.cast(None, jsii.invoke(self, "associateAttributeGroup", [attribute_group]))

    @jsii.member(jsii_name="associateStack")
    def associate_stack(self, stack: aws_cdk.Stack) -> None:
        '''(experimental) Associate a stack with the application If the resource is already associated, it will ignore duplicate request.

        A stack can only be associated with one application.

        :param stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Application.associate_stack)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "associateStack", [stack]))

    @jsii.member(jsii_name="generateUniqueHash")
    def _generate_unique_hash(self, resource_address: builtins.str) -> builtins.str:
        '''(experimental) Create a unique id.

        :param resource_address: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Application._generate_unique_hash)
            check_type(argname="argument resource_address", value=resource_address, expected_type=type_hints["resource_address"])
        return typing.cast(builtins.str, jsii.invoke(self, "generateUniqueHash", [resource_address]))

    @jsii.member(jsii_name="shareApplication")
    def share_application(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        share_permission: typing.Optional[typing.Union[builtins.str, SharePermission]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''(experimental) Share an application with accounts, organizations and OUs, and IAM roles and users.

        The application will become available to end users within those principals.

        :param accounts: (experimental) A list of AWS accounts that the application will be shared with. Default: - No accounts specified for share
        :param organization_arns: (experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with. Default: - No AWS Organizations or OUs specified for share
        :param roles: (experimental) A list of AWS IAM roles that the application will be shared with. Default: - No IAM roles specified for share
        :param share_permission: (experimental) An option to manage access to the application or attribute group. Default: - Principals will be assigned read only permissions on the application or attribute group.
        :param users: (experimental) A list of AWS IAM users that the application will be shared with. Default: - No IAM Users specified for share

        :stability: experimental
        '''
        share_options = ShareOptions(
            accounts=accounts,
            organization_arns=organization_arns,
            roles=roles,
            share_permission=share_permission,
            users=users,
        )

        return typing.cast(None, jsii.invoke(self, "shareApplication", [share_options]))

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''(experimental) The ID of the application.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))


@jsii.implements(IAttributeGroup)
class AttributeGroup(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicecatalogappregistry-alpha.AttributeGroup",
):
    '''(experimental) A Service Catalog AppRegistry Attribute Group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        attribute_group = appreg.AttributeGroup(self, "MyFirstAttributeGroup",
            attribute_group_name="MyFirstAttributeGroupName",
            description="description for my attribute group",  # the description is optional,
            attributes={
                "project": "foo",
                "team": ["member1", "member2", "member3"],
                "public": False,
                "stages": {
                    "alpha": "complete",
                    "beta": "incomplete",
                    "release": "not started"
                }
            }
        )
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        attribute_group_name: builtins.str,
        attributes: typing.Mapping[builtins.str, typing.Any],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param attribute_group_name: (experimental) Enforces a particular physical attribute group name.
        :param attributes: (experimental) A JSON of nested key-value pairs that represent the attributes in the group. Attributes maybe an empty JSON '{}', but must be explicitly stated.
        :param description: (experimental) Description for attribute group. Default: - No description provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttributeGroup.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AttributeGroupProps(
            attribute_group_name=attribute_group_name,
            attributes=attributes,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAttributeGroupArn")
    @builtins.classmethod
    def from_attribute_group_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        attribute_group_arn: builtins.str,
    ) -> IAttributeGroup:
        '''(experimental) Imports an attribute group construct that represents an external attribute group.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param attribute_group_arn: the Amazon Resource Name of the existing AppRegistry attribute group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AttributeGroup.from_attribute_group_arn)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument attribute_group_arn", value=attribute_group_arn, expected_type=type_hints["attribute_group_arn"])
        return typing.cast(IAttributeGroup, jsii.sinvoke(cls, "fromAttributeGroupArn", [scope, id, attribute_group_arn]))

    @jsii.member(jsii_name="getAttributeGroupSharePermissionARN")
    def _get_attribute_group_share_permission_arn(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        share_permission: typing.Optional[typing.Union[builtins.str, SharePermission]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> builtins.str:
        '''(experimental) Get the correct permission ARN based on the SharePermission.

        :param accounts: (experimental) A list of AWS accounts that the application will be shared with. Default: - No accounts specified for share
        :param organization_arns: (experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with. Default: - No AWS Organizations or OUs specified for share
        :param roles: (experimental) A list of AWS IAM roles that the application will be shared with. Default: - No IAM roles specified for share
        :param share_permission: (experimental) An option to manage access to the application or attribute group. Default: - Principals will be assigned read only permissions on the application or attribute group.
        :param users: (experimental) A list of AWS IAM users that the application will be shared with. Default: - No IAM Users specified for share

        :stability: experimental
        '''
        share_options = ShareOptions(
            accounts=accounts,
            organization_arns=organization_arns,
            roles=roles,
            share_permission=share_permission,
            users=users,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "getAttributeGroupSharePermissionARN", [share_options]))

    @jsii.member(jsii_name="shareAttributeGroup")
    def share_attribute_group(
        self,
        *,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IRole]] = None,
        share_permission: typing.Optional[typing.Union[builtins.str, SharePermission]] = None,
        users: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IUser]] = None,
    ) -> None:
        '''(experimental) Share the attribute group resource with other IAM entities, accounts, or OUs.

        :param accounts: (experimental) A list of AWS accounts that the application will be shared with. Default: - No accounts specified for share
        :param organization_arns: (experimental) A list of AWS Organization or Organizational Units (OUs) ARNs that the application will be shared with. Default: - No AWS Organizations or OUs specified for share
        :param roles: (experimental) A list of AWS IAM roles that the application will be shared with. Default: - No IAM roles specified for share
        :param share_permission: (experimental) An option to manage access to the application or attribute group. Default: - Principals will be assigned read only permissions on the application or attribute group.
        :param users: (experimental) A list of AWS IAM users that the application will be shared with. Default: - No IAM Users specified for share

        :stability: experimental
        '''
        share_options = ShareOptions(
            accounts=accounts,
            organization_arns=organization_arns,
            roles=roles,
            share_permission=share_permission,
            users=users,
        )

        return typing.cast(None, jsii.invoke(self, "shareAttributeGroup", [share_options]))

    @builtins.property
    @jsii.member(jsii_name="attributeGroupArn")
    def attribute_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the attribute group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="attributeGroupId")
    def attribute_group_id(self) -> builtins.str:
        '''(experimental) The ID of the attribute group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "attributeGroupId"))


__all__ = [
    "Application",
    "ApplicationProps",
    "AttributeGroup",
    "AttributeGroupProps",
    "IApplication",
    "IAttributeGroup",
    "ShareOptions",
    "SharePermission",
]

publication.publish()
