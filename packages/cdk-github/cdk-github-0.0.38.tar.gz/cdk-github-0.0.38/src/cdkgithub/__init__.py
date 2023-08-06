'''
[![npm version](https://badge.fury.io/js/cdk-github.svg)](https://badge.fury.io/js/cdk-github)
[![PyPI version](https://badge.fury.io/py/cdk-github.svg)](https://badge.fury.io/py/cdk-github)
[![NuGet version](https://badge.fury.io/nu/cdkgithub.svg)](https://badge.fury.io/nu/cdkgithub)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/io.github.wtfjoke/cdk-github/badge.svg)](https://maven-badges.herokuapp.com/maven-central/io.github.wtfjoke/cdk-github/)
[![release](https://github.com/wtfjoke/cdk-github/actions/workflows/release.yml/badge.svg)](https://github.com/wtfjoke/cdk-github/actions/workflows/release.yml)
![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge) [![View on Construct Hub](https://constructs.dev/badge?package=cdk-github)](https://constructs.dev/packages/cdk-github)

# CDK-GitHub

GitHub Constructs for use in [AWS CDK](https://aws.amazon.com/cdk/) .

This project aims to make GitHub's API accessible through CDK with various helper constructs to create resources in GitHub.
The target is to replicate most of the functionality of the official [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest/docs).

Internally [AWS CloudFormation custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) and [octokit](https://github.com/octokit/core.js) are used to manage GitHub resources (such as Secrets).

# 🔧 Installation

JavaScript/TypeScript:
`npm install cdk-github`

Python:
`pip install cdk-github`

Java

<details>
  <summary>Maven:</summary>

```xml
<dependency>
  <groupId>io.github.wtfjoke</groupId>
  <artifactId>cdk-github</artifactId>
  <version>VERSION</version>
</dependency>
```

</details>
<details>
  <summary>Gradle:</summary>

`implementation 'io.github.wtfjoke:cdk-github:VERSION'`

</details>
<details>
  <summary>Gradle (Kotlin):</summary>

`implementation("io.github.wtfjoke:cdk-github:VERSION")`

</details>

C#
See https://www.nuget.org/packages/CdkGithub

# 📚 Constructs

This library provides the following constructs:

* [ActionEnvironmentSecret](API.md#actionenvironmentsecret-) - Creates a [GitHub Action environment secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-an-environment) from a given AWS Secrets Manager secret.
* [ActionSecret](API.md#actionsecret-) - Creates a [GitHub Action (repository) secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) from a given AWS Secrets Manager secret.
* [GitHubResource](API.md#githubresource-) - Creates an arbitrary GitHub resource. When no suitable construct fits your needs, this construct can be used to create most GitHub resources. It is an L1 construct.

# 🔓 Authentication

Currently the constructs only support authentication via a [GitHub Personal Access Token](https://github.com/settings/tokens/new). The token needs to be a stored in a AWS SecretsManager Secret and passed to the construct as parameter.

# 👩‍🏫 Examples

The API documentation and examples in different languages are available on [Construct Hub](https://constructs.dev/packages/cdk-github).
All (typescript) examples can be found in the folder [examples](src/examples/).

## ActionSecret

```python
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { ActionSecret } from 'cdk-github';

export class ActionSecretStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const githubTokenSecret = Secret.fromSecretNameV2(this, 'ghSecret', 'GITHUB_TOKEN');
    const sourceSecret = Secret.fromSecretNameV2(this, 'secretToStoreInGitHub', 'testcdkgithub');

    new ActionSecret(this, 'GitHubActionSecret', {
      githubTokenSecret,
      repository: { name: 'cdk-github', owner: 'wtfjoke' },
      repositorySecretName: 'A_RANDOM_GITHUB_SECRET',
      sourceSecret,
    });
  }
}
```

## ActionEnvironmentSecret

```python
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { ActionEnvironmentSecret } from 'cdk-github';

export class ActionEnvironmentSecretStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const githubTokenSecret = Secret.fromSecretNameV2(this, 'ghSecret', 'GITHUB_TOKEN');
    const sourceSecret = Secret.fromSecretNameV2(this, 'secretToStoreInGitHub', 'testcdkgithub');

    new ActionEnvironmentSecret(this, 'GitHubActionEnvironmentSecret', {
      githubTokenSecret,
      environment: 'dev',
      repository: { name: 'cdk-github', owner: 'wtfjoke' },
      repositorySecretName: 'A_RANDOM_GITHUB_SECRET',
      sourceSecret,
    });
  }
}
```

## GitHubResource

```python
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { StringParameter } from 'aws-cdk-lib/aws-ssm';
import { GitHubResource } from 'cdk-github';


export class GitHubResourceIssueStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const githubTokenSecret = Secret.fromSecretNameV2(this, 'ghSecret', 'GITHUB_TOKEN');
    // optional
    const writeResponseToSSMParameter = StringParameter.fromSecureStringParameterAttributes(this, 'responseBody', { parameterName: '/cdk-github/encrypted-response' });

    new GitHubResource(this, 'GitHubIssue', {
      githubTokenSecret,
      createRequestEndpoint: 'POST /repos/WtfJoke/dummytest/issues',
      createRequestPayload: JSON.stringify({ title: 'Testing cdk-github', body: "I'm opening an issue by using aws cdk 🎉", labels: ['bug'] }),
      createRequestResultParameter: 'number',
      deleteRequestEndpoint: 'PATCH /repos/WtfJoke/dummytest/issues/:number',
      deleteRequestPayload: JSON.stringify({ state: 'closed' }),
      writeResponseToSSMParameter,
    });
  }
}
```

# 💖 Contributing

Contributions of all kinds are welcome! Check out our [contributing guide](CONTRIBUTING.md).
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

import aws_cdk.aws_secretsmanager
import aws_cdk.aws_ssm
import constructs


class ActionEnvironmentSecret(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github.ActionEnvironmentSecret",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        environment: builtins.str,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository: "IGitHubRepository",
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
        source_secret_json_field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param environment: (experimental) The GithHub environment name which the secret should be stored in.
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository: (experimental) The GitHub repository information (owner and name).
        :param repository_secret_name: (experimental) The GitHub secret name to be stored.
        :param source_secret: (experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).
        :param source_secret_json_field: (experimental) The key of a JSON field to retrieve in sourceSecret. This can only be used if the secret stores a JSON object. Default: - returns all the content stored in the Secrets Manager secret.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ActionEnvironmentSecret.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ActionEnvironmentSecretProps(
            environment=environment,
            github_token_secret=github_token_secret,
            repository=repository,
            repository_secret_name=repository_secret_name,
            source_secret=source_secret,
            source_secret_json_field=source_secret_json_field,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-github.ActionEnvironmentSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "environment": "environment",
        "github_token_secret": "githubTokenSecret",
        "repository": "repository",
        "repository_secret_name": "repositorySecretName",
        "source_secret": "sourceSecret",
        "source_secret_json_field": "sourceSecretJsonField",
    },
)
class ActionEnvironmentSecretProps:
    def __init__(
        self,
        *,
        environment: builtins.str,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository: "IGitHubRepository",
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
        source_secret_json_field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param environment: (experimental) The GithHub environment name which the secret should be stored in.
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository: (experimental) The GitHub repository information (owner and name).
        :param repository_secret_name: (experimental) The GitHub secret name to be stored.
        :param source_secret: (experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).
        :param source_secret_json_field: (experimental) The key of a JSON field to retrieve in sourceSecret. This can only be used if the secret stores a JSON object. Default: - returns all the content stored in the Secrets Manager secret.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ActionEnvironmentSecretProps.__init__)
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument github_token_secret", value=github_token_secret, expected_type=type_hints["github_token_secret"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_secret_name", value=repository_secret_name, expected_type=type_hints["repository_secret_name"])
            check_type(argname="argument source_secret", value=source_secret, expected_type=type_hints["source_secret"])
            check_type(argname="argument source_secret_json_field", value=source_secret_json_field, expected_type=type_hints["source_secret_json_field"])
        self._values: typing.Dict[str, typing.Any] = {
            "environment": environment,
            "github_token_secret": github_token_secret,
            "repository": repository,
            "repository_secret_name": repository_secret_name,
            "source_secret": source_secret,
        }
        if source_secret_json_field is not None:
            self._values["source_secret_json_field"] = source_secret_json_field

    @builtins.property
    def environment(self) -> builtins.str:
        '''(experimental) The GithHub environment name which the secret should be stored in.

        :stability: experimental
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def github_token_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.

        :stability: experimental
        '''
        result = self._values.get("github_token_secret")
        assert result is not None, "Required property 'github_token_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def repository(self) -> "IGitHubRepository":
        '''(experimental) The GitHub repository information (owner and name).

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast("IGitHubRepository", result)

    @builtins.property
    def repository_secret_name(self) -> builtins.str:
        '''(experimental) The GitHub secret name to be stored.

        :stability: experimental
        '''
        result = self._values.get("repository_secret_name")
        assert result is not None, "Required property 'repository_secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).

        :stability: experimental
        '''
        result = self._values.get("source_secret")
        assert result is not None, "Required property 'source_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def source_secret_json_field(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of a JSON field to retrieve in sourceSecret.

        This can only be used if the secret stores a JSON object.

        :default: - returns all the content stored in the Secrets Manager secret.

        :stability: experimental
        '''
        result = self._values.get("source_secret_json_field")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionEnvironmentSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionSecret(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github.ActionSecret",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository: "IGitHubRepository",
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
        source_secret_json_field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository: (experimental) The GitHub repository information (owner and name).
        :param repository_secret_name: (experimental) The GitHub secret name to be stored.
        :param source_secret: (experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).
        :param source_secret_json_field: (experimental) The key of a JSON field to retrieve in sourceSecret. This can only be used if the secret stores a JSON object. Default: - returns all the content stored in the Secrets Manager secret.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ActionSecret.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ActionSecretProps(
            github_token_secret=github_token_secret,
            repository=repository,
            repository_secret_name=repository_secret_name,
            source_secret=source_secret,
            source_secret_json_field=source_secret_json_field,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-github.ActionSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "github_token_secret": "githubTokenSecret",
        "repository": "repository",
        "repository_secret_name": "repositorySecretName",
        "source_secret": "sourceSecret",
        "source_secret_json_field": "sourceSecretJsonField",
    },
)
class ActionSecretProps:
    def __init__(
        self,
        *,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository: "IGitHubRepository",
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
        source_secret_json_field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository: (experimental) The GitHub repository information (owner and name).
        :param repository_secret_name: (experimental) The GitHub secret name to be stored.
        :param source_secret: (experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).
        :param source_secret_json_field: (experimental) The key of a JSON field to retrieve in sourceSecret. This can only be used if the secret stores a JSON object. Default: - returns all the content stored in the Secrets Manager secret.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ActionSecretProps.__init__)
            check_type(argname="argument github_token_secret", value=github_token_secret, expected_type=type_hints["github_token_secret"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_secret_name", value=repository_secret_name, expected_type=type_hints["repository_secret_name"])
            check_type(argname="argument source_secret", value=source_secret, expected_type=type_hints["source_secret"])
            check_type(argname="argument source_secret_json_field", value=source_secret_json_field, expected_type=type_hints["source_secret_json_field"])
        self._values: typing.Dict[str, typing.Any] = {
            "github_token_secret": github_token_secret,
            "repository": repository,
            "repository_secret_name": repository_secret_name,
            "source_secret": source_secret,
        }
        if source_secret_json_field is not None:
            self._values["source_secret_json_field"] = source_secret_json_field

    @builtins.property
    def github_token_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.

        :stability: experimental
        '''
        result = self._values.get("github_token_secret")
        assert result is not None, "Required property 'github_token_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def repository(self) -> "IGitHubRepository":
        '''(experimental) The GitHub repository information (owner and name).

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast("IGitHubRepository", result)

    @builtins.property
    def repository_secret_name(self) -> builtins.str:
        '''(experimental) The GitHub secret name to be stored.

        :stability: experimental
        '''
        result = self._values.get("repository_secret_name")
        assert result is not None, "Required property 'repository_secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) This AWS secret value will be stored in GitHub as a secret (under the name of repositorySecretName).

        :stability: experimental
        '''
        result = self._values.get("source_secret")
        assert result is not None, "Required property 'source_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def source_secret_json_field(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of a JSON field to retrieve in sourceSecret.

        This can only be used if the secret stores a JSON object.

        :default: - returns all the content stored in the Secrets Manager secret.

        :stability: experimental
        '''
        result = self._values.get("source_secret_json_field")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubResource(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github.GitHubResource",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        create_request_endpoint: builtins.str,
        delete_request_endpoint: builtins.str,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        create_request_payload: typing.Optional[builtins.str] = None,
        create_request_result_parameter: typing.Optional[builtins.str] = None,
        delete_request_payload: typing.Optional[builtins.str] = None,
        update_request_endpoint: typing.Optional[builtins.str] = None,
        update_request_payload: typing.Optional[builtins.str] = None,
        write_response_to_ssm_parameter: typing.Optional[aws_cdk.aws_ssm.IParameter] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param create_request_endpoint: (experimental) The GitHub api endpoint url for creating resources in format: ``POST /repos/OWNER/REPO/issues``. This is called when the GitHubResource is created. Example:: const createRequestEndpoint = 'POST /repos/octocat/Hello-World/issues'
        :param delete_request_endpoint: (experimental) The GitHub api endpoint url to delete this resource in format: ``POST /repos/OWNER/REPO/issues``. This is called when the GitHubResource is deleted/destroyed. Example:: const deleteRequestEndpoint = 'PATCH repos/octocat/Hello-World/issues/1' If you want to use the @see {@link GitHubResourceProps#createRequestResultParameter}, you can use the following syntax (assuming you have set createRequestResultParameter to ``"number"``):: const deleteRequestEndpoint = 'PATCH repos/octocat/Hello-World/:number'
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param create_request_payload: (experimental) The GitHub api request payload for creating resources. This is a JSON parseable string. Used for @see {@link GitHubResourceProps#createRequestEndpoint}. Example:: const createRequestPayload = JSON.stringify({ title: 'Found a bug', body: "I'm having a problem with this.", assignees: ['octocat'], milestone: 1, labels: ['bug'] })
        :param create_request_result_parameter: (experimental) Used to extract a value from the result of the createRequest(Endpoint) to be used in update/deleteRequests. Example: ``"number"`` (for the issue number) When this parameter is set and can be extracted from the result, the extracted value will be used for the PhyscialResourceId of the CustomResource. Changing the parameter once the stack is deployed is not supported.
        :param delete_request_payload: (experimental) The GitHub api request payload to delete this resource. This is a JSON parseable string. Used for @see {@link GitHubResourceProps#deleteRequestEndpoint}. Example:: const deleteRequestPayload = JSON.stringify({ state: 'closed' })
        :param update_request_endpoint: (experimental) The GitHub api endpoint url to update this resource in format: ``POST /repos/OWNER/REPO/issues``. This is called when the GitHubResource is updated. In most of the cases you want to either omit this or use the same value as createRequestEndpoint. Example:: const updateRequestEndpoint = 'PATCH repos/octocat/Hello-World/issues/1' If you want to use the @see {@link GitHubResourceProps#createRequestResultParameter}, you can use the following syntax (assuming you have set createRequestResultParameter to ``"number"``):: const updateRequestEndpoint = 'PATCH repos/octocat/Hello-World/:number'
        :param update_request_payload: (experimental) The GitHub api request payload to update this resources. This is a JSON parseable string. Used for @see {@link GitHubResourceProps#createRequestEndpoint}. Example:: const updateRequestPayload = JSON.stringify({ title: 'Found a bug', body: "I'm having a problem with this.", assignees: ['octocat'], milestone: 1, state: 'open', labels: ['bug'] })
        :param write_response_to_ssm_parameter: (experimental) The response body of the last GitHub api request will be written to this ssm parameter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GitHubResource.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubResourceProps(
            create_request_endpoint=create_request_endpoint,
            delete_request_endpoint=delete_request_endpoint,
            github_token_secret=github_token_secret,
            create_request_payload=create_request_payload,
            create_request_result_parameter=create_request_result_parameter,
            delete_request_payload=delete_request_payload,
            update_request_endpoint=update_request_endpoint,
            update_request_payload=update_request_payload,
            write_response_to_ssm_parameter=write_response_to_ssm_parameter,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-github.GitHubResourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_request_endpoint": "createRequestEndpoint",
        "delete_request_endpoint": "deleteRequestEndpoint",
        "github_token_secret": "githubTokenSecret",
        "create_request_payload": "createRequestPayload",
        "create_request_result_parameter": "createRequestResultParameter",
        "delete_request_payload": "deleteRequestPayload",
        "update_request_endpoint": "updateRequestEndpoint",
        "update_request_payload": "updateRequestPayload",
        "write_response_to_ssm_parameter": "writeResponseToSSMParameter",
    },
)
class GitHubResourceProps:
    def __init__(
        self,
        *,
        create_request_endpoint: builtins.str,
        delete_request_endpoint: builtins.str,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        create_request_payload: typing.Optional[builtins.str] = None,
        create_request_result_parameter: typing.Optional[builtins.str] = None,
        delete_request_payload: typing.Optional[builtins.str] = None,
        update_request_endpoint: typing.Optional[builtins.str] = None,
        update_request_payload: typing.Optional[builtins.str] = None,
        write_response_to_ssm_parameter: typing.Optional[aws_cdk.aws_ssm.IParameter] = None,
    ) -> None:
        '''
        :param create_request_endpoint: (experimental) The GitHub api endpoint url for creating resources in format: ``POST /repos/OWNER/REPO/issues``. This is called when the GitHubResource is created. Example:: const createRequestEndpoint = 'POST /repos/octocat/Hello-World/issues'
        :param delete_request_endpoint: (experimental) The GitHub api endpoint url to delete this resource in format: ``POST /repos/OWNER/REPO/issues``. This is called when the GitHubResource is deleted/destroyed. Example:: const deleteRequestEndpoint = 'PATCH repos/octocat/Hello-World/issues/1' If you want to use the @see {@link GitHubResourceProps#createRequestResultParameter}, you can use the following syntax (assuming you have set createRequestResultParameter to ``"number"``):: const deleteRequestEndpoint = 'PATCH repos/octocat/Hello-World/:number'
        :param github_token_secret: (experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param create_request_payload: (experimental) The GitHub api request payload for creating resources. This is a JSON parseable string. Used for @see {@link GitHubResourceProps#createRequestEndpoint}. Example:: const createRequestPayload = JSON.stringify({ title: 'Found a bug', body: "I'm having a problem with this.", assignees: ['octocat'], milestone: 1, labels: ['bug'] })
        :param create_request_result_parameter: (experimental) Used to extract a value from the result of the createRequest(Endpoint) to be used in update/deleteRequests. Example: ``"number"`` (for the issue number) When this parameter is set and can be extracted from the result, the extracted value will be used for the PhyscialResourceId of the CustomResource. Changing the parameter once the stack is deployed is not supported.
        :param delete_request_payload: (experimental) The GitHub api request payload to delete this resource. This is a JSON parseable string. Used for @see {@link GitHubResourceProps#deleteRequestEndpoint}. Example:: const deleteRequestPayload = JSON.stringify({ state: 'closed' })
        :param update_request_endpoint: (experimental) The GitHub api endpoint url to update this resource in format: ``POST /repos/OWNER/REPO/issues``. This is called when the GitHubResource is updated. In most of the cases you want to either omit this or use the same value as createRequestEndpoint. Example:: const updateRequestEndpoint = 'PATCH repos/octocat/Hello-World/issues/1' If you want to use the @see {@link GitHubResourceProps#createRequestResultParameter}, you can use the following syntax (assuming you have set createRequestResultParameter to ``"number"``):: const updateRequestEndpoint = 'PATCH repos/octocat/Hello-World/:number'
        :param update_request_payload: (experimental) The GitHub api request payload to update this resources. This is a JSON parseable string. Used for @see {@link GitHubResourceProps#createRequestEndpoint}. Example:: const updateRequestPayload = JSON.stringify({ title: 'Found a bug', body: "I'm having a problem with this.", assignees: ['octocat'], milestone: 1, state: 'open', labels: ['bug'] })
        :param write_response_to_ssm_parameter: (experimental) The response body of the last GitHub api request will be written to this ssm parameter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GitHubResourceProps.__init__)
            check_type(argname="argument create_request_endpoint", value=create_request_endpoint, expected_type=type_hints["create_request_endpoint"])
            check_type(argname="argument delete_request_endpoint", value=delete_request_endpoint, expected_type=type_hints["delete_request_endpoint"])
            check_type(argname="argument github_token_secret", value=github_token_secret, expected_type=type_hints["github_token_secret"])
            check_type(argname="argument create_request_payload", value=create_request_payload, expected_type=type_hints["create_request_payload"])
            check_type(argname="argument create_request_result_parameter", value=create_request_result_parameter, expected_type=type_hints["create_request_result_parameter"])
            check_type(argname="argument delete_request_payload", value=delete_request_payload, expected_type=type_hints["delete_request_payload"])
            check_type(argname="argument update_request_endpoint", value=update_request_endpoint, expected_type=type_hints["update_request_endpoint"])
            check_type(argname="argument update_request_payload", value=update_request_payload, expected_type=type_hints["update_request_payload"])
            check_type(argname="argument write_response_to_ssm_parameter", value=write_response_to_ssm_parameter, expected_type=type_hints["write_response_to_ssm_parameter"])
        self._values: typing.Dict[str, typing.Any] = {
            "create_request_endpoint": create_request_endpoint,
            "delete_request_endpoint": delete_request_endpoint,
            "github_token_secret": github_token_secret,
        }
        if create_request_payload is not None:
            self._values["create_request_payload"] = create_request_payload
        if create_request_result_parameter is not None:
            self._values["create_request_result_parameter"] = create_request_result_parameter
        if delete_request_payload is not None:
            self._values["delete_request_payload"] = delete_request_payload
        if update_request_endpoint is not None:
            self._values["update_request_endpoint"] = update_request_endpoint
        if update_request_payload is not None:
            self._values["update_request_payload"] = update_request_payload
        if write_response_to_ssm_parameter is not None:
            self._values["write_response_to_ssm_parameter"] = write_response_to_ssm_parameter

    @builtins.property
    def create_request_endpoint(self) -> builtins.str:
        '''(experimental) The GitHub api endpoint url for creating resources in format: ``POST /repos/OWNER/REPO/issues``.

        This is called when the GitHubResource is created.

        Example::

           const createRequestEndpoint = 'POST /repos/octocat/Hello-World/issues'

        :stability: experimental
        '''
        result = self._values.get("create_request_endpoint")
        assert result is not None, "Required property 'create_request_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_request_endpoint(self) -> builtins.str:
        '''(experimental) The GitHub api endpoint url to delete this resource in format: ``POST /repos/OWNER/REPO/issues``.

        This is called when the GitHubResource is deleted/destroyed.

        Example::

           const deleteRequestEndpoint = 'PATCH repos/octocat/Hello-World/issues/1'

        If you want to use the  @see {@link GitHubResourceProps#createRequestResultParameter}, you can use the following syntax (assuming you have set createRequestResultParameter to ``"number"``)::

           const deleteRequestEndpoint = 'PATCH repos/octocat/Hello-World/:number'

        :stability: experimental
        '''
        result = self._values.get("delete_request_endpoint")
        assert result is not None, "Required property 'delete_request_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def github_token_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) The AWS secret in which the OAuth GitHub (personal) access token is stored.

        :stability: experimental
        '''
        result = self._values.get("github_token_secret")
        assert result is not None, "Required property 'github_token_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def create_request_payload(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub api request payload for creating resources. This is a JSON parseable string.

        Used for  @see {@link GitHubResourceProps#createRequestEndpoint}.

        Example::

           const createRequestPayload = JSON.stringify({ title: 'Found a bug', body: "I'm having a problem with this.", assignees: ['octocat'], milestone: 1, labels: ['bug'] })

        :stability: experimental
        '''
        result = self._values.get("create_request_payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_request_result_parameter(self) -> typing.Optional[builtins.str]:
        '''(experimental) Used to extract a value from the result of the createRequest(Endpoint) to be used in update/deleteRequests.

        Example: ``"number"`` (for the issue number)

        When this parameter is set and can be extracted from the result, the extracted value will be used for the PhyscialResourceId of the CustomResource.
        Changing the parameter once the stack is deployed is not supported.

        :stability: experimental
        '''
        result = self._values.get("create_request_result_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_request_payload(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub api request payload to delete this resource. This is a JSON parseable string.

        Used for  @see {@link GitHubResourceProps#deleteRequestEndpoint}.

        Example::

           const deleteRequestPayload = JSON.stringify({ state: 'closed' })

        :stability: experimental
        '''
        result = self._values.get("delete_request_payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_request_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub api endpoint url to update this resource in format: ``POST /repos/OWNER/REPO/issues``.

        This is called when the GitHubResource is updated.

        In most of the cases you want to either omit this or use the same value as createRequestEndpoint.

        Example::

           const updateRequestEndpoint = 'PATCH repos/octocat/Hello-World/issues/1'

        If you want to use the  @see {@link GitHubResourceProps#createRequestResultParameter}, you can use the following syntax (assuming you have set createRequestResultParameter to ``"number"``)::

           const updateRequestEndpoint = 'PATCH repos/octocat/Hello-World/:number'

        :stability: experimental
        '''
        result = self._values.get("update_request_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_request_payload(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub api request payload to update this resources. This is a JSON parseable string.

        Used for  @see {@link GitHubResourceProps#createRequestEndpoint}.

        Example::

           const updateRequestPayload = JSON.stringify({ title: 'Found a bug', body: "I'm having a problem with this.", assignees: ['octocat'], milestone: 1, state: 'open', labels: ['bug'] })

        :stability: experimental
        '''
        result = self._values.get("update_request_payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def write_response_to_ssm_parameter(
        self,
    ) -> typing.Optional[aws_cdk.aws_ssm.IParameter]:
        '''(experimental) The response body of the last GitHub api request will be written to this ssm parameter.

        :stability: experimental
        '''
        result = self._values.get("write_response_to_ssm_parameter")
        return typing.cast(typing.Optional[aws_cdk.aws_ssm.IParameter], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-github.IGitHubRepository")
class IGitHubRepository(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The GitHub repository name.

        :stability: experimental
        '''
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub repository owner.

        :default: - user account which owns the personal access token

        :stability: experimental
        '''
        ...

    @owner.setter
    def owner(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IGitHubRepositoryProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-github.IGitHubRepository"

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The GitHub repository name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(IGitHubRepository, "name").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub repository owner.

        :default: - user account which owns the personal access token

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(IGitHubRepository, "owner").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGitHubRepository).__jsii_proxy_class__ = lambda : _IGitHubRepositoryProxy


__all__ = [
    "ActionEnvironmentSecret",
    "ActionEnvironmentSecretProps",
    "ActionSecret",
    "ActionSecretProps",
    "GitHubResource",
    "GitHubResourceProps",
    "IGitHubRepository",
]

publication.publish()
