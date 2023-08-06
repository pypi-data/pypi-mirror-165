"""
Type annotations for identitystore service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_identitystore.client import IdentityStoreClient

    session = Session()
    client: IdentityStoreClient = session.client("identitystore")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListGroupMembershipsForMemberPaginator,
    ListGroupMembershipsPaginator,
    ListGroupsPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AddressTypeDef,
    AlternateIdentifierTypeDef,
    AttributeOperationTypeDef,
    CreateGroupMembershipResponseTypeDef,
    CreateGroupResponseTypeDef,
    CreateUserResponseTypeDef,
    DescribeGroupMembershipResponseTypeDef,
    DescribeGroupResponseTypeDef,
    DescribeUserResponseTypeDef,
    EmailTypeDef,
    FilterTypeDef,
    GetGroupIdResponseTypeDef,
    GetGroupMembershipIdResponseTypeDef,
    GetUserIdResponseTypeDef,
    IsMemberInGroupsResponseTypeDef,
    ListGroupMembershipsForMemberResponseTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListUsersResponseTypeDef,
    MemberIdTypeDef,
    NameTypeDef,
    PhoneNumberTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IdentityStoreClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IdentityStoreClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IdentityStoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#close)
        """

    def create_group(
        self, *, IdentityStoreId: str, DisplayName: str = ..., Description: str = ...
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a group within the specified identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.create_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#create_group)
        """

    def create_group_membership(
        self, *, IdentityStoreId: str, GroupId: str, MemberId: MemberIdTypeDef
    ) -> CreateGroupMembershipResponseTypeDef:
        """
        Creates a relationship between a member and a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.create_group_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#create_group_membership)
        """

    def create_user(
        self,
        *,
        IdentityStoreId: str,
        UserName: str = ...,
        Name: NameTypeDef = ...,
        DisplayName: str = ...,
        NickName: str = ...,
        ProfileUrl: str = ...,
        Emails: Sequence[EmailTypeDef] = ...,
        Addresses: Sequence[AddressTypeDef] = ...,
        PhoneNumbers: Sequence[PhoneNumberTypeDef] = ...,
        UserType: str = ...,
        Title: str = ...,
        PreferredLanguage: str = ...,
        Locale: str = ...,
        Timezone: str = ...
    ) -> CreateUserResponseTypeDef:
        """
        Creates a new user within the specified identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.create_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#create_user)
        """

    def delete_group(self, *, IdentityStoreId: str, GroupId: str) -> Dict[str, Any]:
        """
        Delete a group within an identity store given `GroupId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.delete_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#delete_group)
        """

    def delete_group_membership(self, *, IdentityStoreId: str, MembershipId: str) -> Dict[str, Any]:
        """
        Delete a membership within a group given `MembershipId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.delete_group_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#delete_group_membership)
        """

    def delete_user(self, *, IdentityStoreId: str, UserId: str) -> Dict[str, Any]:
        """
        Deletes a user within an identity store given `UserId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.delete_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#delete_user)
        """

    def describe_group(self, *, IdentityStoreId: str, GroupId: str) -> DescribeGroupResponseTypeDef:
        """
        Retrieves the group metadata and attributes from `GroupId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.describe_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#describe_group)
        """

    def describe_group_membership(
        self, *, IdentityStoreId: str, MembershipId: str
    ) -> DescribeGroupMembershipResponseTypeDef:
        """
        Retrieves membership metadata and attributes from `MembershipId` in a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.describe_group_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#describe_group_membership)
        """

    def describe_user(self, *, IdentityStoreId: str, UserId: str) -> DescribeUserResponseTypeDef:
        """
        Retrieves the user metadata and attributes from the `UserId` in an identity
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.describe_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#describe_user)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#generate_presigned_url)
        """

    def get_group_id(
        self, *, IdentityStoreId: str, AlternateIdentifier: AlternateIdentifierTypeDef
    ) -> GetGroupIdResponseTypeDef:
        """
        Retrieves `GroupId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_group_id)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#get_group_id)
        """

    def get_group_membership_id(
        self, *, IdentityStoreId: str, GroupId: str, MemberId: MemberIdTypeDef
    ) -> GetGroupMembershipIdResponseTypeDef:
        """
        Retrieves the `MembershipId` in a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_group_membership_id)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#get_group_membership_id)
        """

    def get_user_id(
        self, *, IdentityStoreId: str, AlternateIdentifier: AlternateIdentifierTypeDef
    ) -> GetUserIdResponseTypeDef:
        """
        Retrieves the `UserId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_user_id)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#get_user_id)
        """

    def is_member_in_groups(
        self, *, IdentityStoreId: str, MemberId: MemberIdTypeDef, GroupIds: Sequence[str]
    ) -> IsMemberInGroupsResponseTypeDef:
        """
        Returns if a member exists in specified groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.is_member_in_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#is_member_in_groups)
        """

    def list_group_memberships(
        self, *, IdentityStoreId: str, GroupId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListGroupMembershipsResponseTypeDef:
        """
        For the specified group in the specified identity store, returns the list of all
        `GroupMembership` objects and returns results in paginated form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_group_memberships)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#list_group_memberships)
        """

    def list_group_memberships_for_member(
        self,
        *,
        IdentityStoreId: str,
        MemberId: MemberIdTypeDef,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListGroupMembershipsForMemberResponseTypeDef:
        """
        For the specified member in the specified identity store, returns the list of
        all `GroupMembership` objects and returns results in paginated form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_group_memberships_for_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#list_group_memberships_for_member)
        """

    def list_groups(
        self,
        *,
        IdentityStoreId: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[FilterTypeDef] = ...
    ) -> ListGroupsResponseTypeDef:
        """
        *Filtering for a group by the group `DisplayName` attribute is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#list_groups)
        """

    def list_users(
        self,
        *,
        IdentityStoreId: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[FilterTypeDef] = ...
    ) -> ListUsersResponseTypeDef:
        """
        *Filtering for a user by the `UserName` attribute is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_users)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#list_users)
        """

    def update_group(
        self, *, IdentityStoreId: str, GroupId: str, Operations: Sequence[AttributeOperationTypeDef]
    ) -> Dict[str, Any]:
        """
        For the specified group in the specified identity store, updates the group
        metadata and attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.update_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#update_group)
        """

    def update_user(
        self, *, IdentityStoreId: str, UserId: str, Operations: Sequence[AttributeOperationTypeDef]
    ) -> Dict[str, Any]:
        """
        For the specified user in the specified identity store, updates the user
        metadata and attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.update_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#update_user)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_memberships"]
    ) -> ListGroupMembershipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_memberships_for_member"]
    ) -> ListGroupMembershipsForMemberPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/client/#get_paginator)
        """
