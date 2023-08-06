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
