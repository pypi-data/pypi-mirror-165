'''
## CDK Docker Image Deployment

This module allows you to copy docker image assets to a repository you control.
This can be necessary if you want to build a Docker image in one CDK app and consume it in a different app or outside the CDK,
or if you want to apply a lifecycle policy to all images of a part of your application.

### Getting Started

Below is a basic example for how to use the `DockerImageDeployment` API:

```python
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as imagedeploy from 'cdk-docker-image-deployment';

const repo = new ecr.Repository.fromRepositoryName(this, 'MyRepository', 'myrepository');

new imagedeploy.DockerImageDeployment(this, 'ExampleImageDeploymentWithTag', {
  source: imagedeploy.Source.directory('path/to/directory'),
  destination: imagedeploy.Destination.ecr(repo, {
    tag: 'myspecialtag',
  });
});
```

### Currently Supported Sources

* `Source.directory()`: Supply a path to a local docker image as source.

> Don't see a source listed? See if there is an open [issue](https://github.com/cdklabs/cdk-docker-image-deployment/issues)
> or [PR](https://github.com/cdklabs/cdk-docker-image-deployment/pulls) already. If not, please open an issue asking for it
> or better yet, submit a contribution!

### Currently Supported Destinations

* `Destination.ecr(repo, options)`: Send your docker image to an ECR repository in your stack's account.

> Don't see a destination listed? See if there is an open [issue](https://github.com/cdklabs/cdk-docker-image-deployment/issues)
> or [PR](https://github.com/cdklabs/cdk-docker-image-deployment/pulls) already. If not, please open an issue asking for it
> or better yet, submit a contribution!

### Under the Hood

1. When this stack is deployed (either via cdk deploy or via CI/CD), the contents of the local Docker image will be archived and uploaded to an intermediary assets ECR Repository using the cdk-assets mechanism.
2. The `DockerImageDeployment` construct synthesizes a CodeBuild Project which uses docker to pull the image from the intermediary repository, tag the image if a tag is provided, and push the image to the destination repository.
3. The deployment will wait until the CodeBuild Project completes successfully before finishing.

The architecture of this construct can be seen here:

![Construct-Architecture](https://user-images.githubusercontent.com/36202692/187282269-7ab29d3e-192f-470f-9123-5dbb62d9dac3.jpg)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
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

import aws_cdk.aws_ecr
import aws_cdk.aws_iam
import constructs


class Destination(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-docker-image-deployment.Destination",
):
    '''Specifies docker image deployment destination.

    Usage::

       declare const repo: ecr.IRepository;
       const destinationEcr = dockerDeploy.Destination.ecr(repository, {
          tag: 'tag',
       });
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="ecr")
    @builtins.classmethod
    def ecr(
        cls,
        repository: aws_cdk.aws_ecr.IRepository,
        *,
        tag: typing.Optional[builtins.str] = None,
    ) -> "Destination":
        '''Uses an ECR repository in the same account as the stack as the destination for the image.

        :param repository: -
        :param tag: Tag of deployed image. Default: - tag of source
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Destination.ecr)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        options = EcrSourceOptions(tag=tag)

        return typing.cast("Destination", jsii.sinvoke(cls, "ecr", [repository, options]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, role: aws_cdk.aws_iam.IGrantable) -> "DestinationConfig":
        '''Bind grants the CodeBuild role permissions to pull and push to a repository if necessary.

        Bind should be invoked by the caller to get the DestinationConfig.

        :param role: -
        '''
        ...


class _DestinationProxy(Destination):
    @jsii.member(jsii_name="bind")
    def bind(self, role: aws_cdk.aws_iam.IGrantable) -> "DestinationConfig":
        '''Bind grants the CodeBuild role permissions to pull and push to a repository if necessary.

        Bind should be invoked by the caller to get the DestinationConfig.

        :param role: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Destination.bind)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast("DestinationConfig", jsii.invoke(self, "bind", [role]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Destination).__jsii_proxy_class__ = lambda : _DestinationProxy


@jsii.data_type(
    jsii_type="cdk-docker-image-deployment.DestinationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "destination_uri": "destinationUri",
        "login_config": "loginConfig",
        "destination_tag": "destinationTag",
    },
)
class DestinationConfig:
    def __init__(
        self,
        *,
        destination_uri: builtins.str,
        login_config: typing.Union["LoginConfig", typing.Dict[str, typing.Any]],
        destination_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Destination information.

        :param destination_uri: The URI of the destination repository to deploy to.
        :param login_config: The login command and region.
        :param destination_tag: The tag of the deployed image. Default: - the tag of the source
        '''
        if isinstance(login_config, dict):
            login_config = LoginConfig(**login_config)
        if __debug__:
            type_hints = typing.get_type_hints(DestinationConfig.__init__)
            check_type(argname="argument destination_uri", value=destination_uri, expected_type=type_hints["destination_uri"])
            check_type(argname="argument login_config", value=login_config, expected_type=type_hints["login_config"])
            check_type(argname="argument destination_tag", value=destination_tag, expected_type=type_hints["destination_tag"])
        self._values: typing.Dict[str, typing.Any] = {
            "destination_uri": destination_uri,
            "login_config": login_config,
        }
        if destination_tag is not None:
            self._values["destination_tag"] = destination_tag

    @builtins.property
    def destination_uri(self) -> builtins.str:
        '''The URI of the destination repository to deploy to.'''
        result = self._values.get("destination_uri")
        assert result is not None, "Required property 'destination_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def login_config(self) -> "LoginConfig":
        '''The login command and region.'''
        result = self._values.get("login_config")
        assert result is not None, "Required property 'login_config' is missing"
        return typing.cast("LoginConfig", result)

    @builtins.property
    def destination_tag(self) -> typing.Optional[builtins.str]:
        '''The tag of the deployed image.

        :default: - the tag of the source
        '''
        result = self._values.get("destination_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerImageDeployment(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-docker-image-deployment.DockerImageDeployment",
):
    '''``DockerImageDeployment`` pushes an image from a local or external source to a specified external destination.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        destination: Destination,
        source: "Source",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param destination: Destination repository to deploy the image to.
        :param source: Source of the image to deploy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DockerImageDeployment.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DockerImageDeploymentProps(destination=destination, source=source)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-docker-image-deployment.DockerImageDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "source": "source"},
)
class DockerImageDeploymentProps:
    def __init__(self, *, destination: Destination, source: "Source") -> None:
        '''
        :param destination: Destination repository to deploy the image to.
        :param source: Source of the image to deploy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DockerImageDeploymentProps.__init__)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[str, typing.Any] = {
            "destination": destination,
            "source": source,
        }

    @builtins.property
    def destination(self) -> Destination:
        '''Destination repository to deploy the image to.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(Destination, result)

    @builtins.property
    def source(self) -> "Source":
        '''Source of the image to deploy.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("Source", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-docker-image-deployment.EcrSourceOptions",
    jsii_struct_bases=[],
    name_mapping={"tag": "tag"},
)
class EcrSourceOptions:
    def __init__(self, *, tag: typing.Optional[builtins.str] = None) -> None:
        '''Properties needed for Source.ecr.

        :param tag: Tag of deployed image. Default: - tag of source
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EcrSourceOptions.__init__)
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[str, typing.Any] = {}
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Tag of deployed image.

        :default: - tag of source
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrSourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-docker-image-deployment.LoginConfig",
    jsii_struct_bases=[],
    name_mapping={"login_command": "loginCommand", "region": "region"},
)
class LoginConfig:
    def __init__(
        self,
        *,
        login_command: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Login commands for specified registry.

        :param login_command: Command to run in codebuild to login. Formatted ``docker login ...``.
        :param region: Region of ECR repository. Default: - undefined if not an ECR repository
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LoginConfig.__init__)
            check_type(argname="argument login_command", value=login_command, expected_type=type_hints["login_command"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[str, typing.Any] = {
            "login_command": login_command,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def login_command(self) -> builtins.str:
        '''Command to run in codebuild to login.

        Formatted ``docker login ...``.
        '''
        result = self._values.get("login_command")
        assert result is not None, "Required property 'login_command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region of ECR repository.

        :default: - undefined if not an ECR repository
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Source(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-docker-image-deployment.Source",
):
    '''Specifies docker image deployment source.

    Usage::

       import * as path from 'path';
       const path = path.join(__dirname, 'path/to/directory');
       const sourceDirectory = Source.directory(path);
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="directory")
    @builtins.classmethod
    def directory(cls, path: builtins.str) -> "Source":
        '''Uses a local image built from a Dockerfile in a local directory as the source.

        :param path: - path to the directory containing your Dockerfile (not a path to a file).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Source.directory)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("Source", jsii.sinvoke(cls, "directory", [path]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: constructs.Construct,
        *,
        handler_role: aws_cdk.aws_iam.IRole,
    ) -> "SourceConfig":
        '''Bind grants the CodeBuild role permissions to pull from a repository if necessary.

        Bind should be invoked by the caller to get the SourceConfig.

        :param scope: -
        :param handler_role: The role for the handler.
        '''
        ...


class _SourceProxy(Source):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        *,
        handler_role: aws_cdk.aws_iam.IRole,
    ) -> "SourceConfig":
        '''Bind grants the CodeBuild role permissions to pull from a repository if necessary.

        Bind should be invoked by the caller to get the SourceConfig.

        :param scope: -
        :param handler_role: The role for the handler.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Source.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = SourceContext(handler_role=handler_role)

        return typing.cast("SourceConfig", jsii.invoke(self, "bind", [scope, context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Source).__jsii_proxy_class__ = lambda : _SourceProxy


@jsii.data_type(
    jsii_type="cdk-docker-image-deployment.SourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "image_tag": "imageTag",
        "image_uri": "imageUri",
        "login_config": "loginConfig",
    },
)
class SourceConfig:
    def __init__(
        self,
        *,
        image_tag: builtins.str,
        image_uri: builtins.str,
        login_config: typing.Union[LoginConfig, typing.Dict[str, typing.Any]],
    ) -> None:
        '''Source information.

        :param image_tag: The source tag.
        :param image_uri: The source image URI.
        :param login_config: The login command and region.
        '''
        if isinstance(login_config, dict):
            login_config = LoginConfig(**login_config)
        if __debug__:
            type_hints = typing.get_type_hints(SourceConfig.__init__)
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument login_config", value=login_config, expected_type=type_hints["login_config"])
        self._values: typing.Dict[str, typing.Any] = {
            "image_tag": image_tag,
            "image_uri": image_uri,
            "login_config": login_config,
        }

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''The source tag.'''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_uri(self) -> builtins.str:
        '''The source image URI.'''
        result = self._values.get("image_uri")
        assert result is not None, "Required property 'image_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def login_config(self) -> LoginConfig:
        '''The login command and region.'''
        result = self._values.get("login_config")
        assert result is not None, "Required property 'login_config' is missing"
        return typing.cast(LoginConfig, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-docker-image-deployment.SourceContext",
    jsii_struct_bases=[],
    name_mapping={"handler_role": "handlerRole"},
)
class SourceContext:
    def __init__(self, *, handler_role: aws_cdk.aws_iam.IRole) -> None:
        '''Bind context for Source.

        :param handler_role: The role for the handler.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SourceContext.__init__)
            check_type(argname="argument handler_role", value=handler_role, expected_type=type_hints["handler_role"])
        self._values: typing.Dict[str, typing.Any] = {
            "handler_role": handler_role,
        }

    @builtins.property
    def handler_role(self) -> aws_cdk.aws_iam.IRole:
        '''The role for the handler.'''
        result = self._values.get("handler_role")
        assert result is not None, "Required property 'handler_role' is missing"
        return typing.cast(aws_cdk.aws_iam.IRole, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Destination",
    "DestinationConfig",
    "DockerImageDeployment",
    "DockerImageDeploymentProps",
    "EcrSourceOptions",
    "LoginConfig",
    "Source",
    "SourceConfig",
    "SourceContext",
]

publication.publish()
