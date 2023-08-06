"""
Type annotations for identitystore service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_identitystore/type_defs/)

Usage::

    ```python
    from mypy_boto3_identitystore.type_defs import AddressTypeDef

    data: AddressTypeDef = {...}
    ```
"""
import sys
from typing import Any, Dict, List, Mapping, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AddressTypeDef",
    "ExternalIdTypeDef",
    "UniqueAttributeTypeDef",
    "AttributeOperationTypeDef",
    "MemberIdTypeDef",
    "ResponseMetadataTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "EmailTypeDef",
    "NameTypeDef",
    "PhoneNumberTypeDef",
    "DeleteGroupMembershipRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeGroupMembershipRequestRequestTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "FilterTypeDef",
    "PaginatorConfigTypeDef",
    "ListGroupMembershipsRequestRequestTypeDef",
    "GroupTypeDef",
    "AlternateIdentifierTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "CreateGroupMembershipRequestRequestTypeDef",
    "GetGroupMembershipIdRequestRequestTypeDef",
    "GroupMembershipExistenceResultTypeDef",
    "GroupMembershipTypeDef",
    "IsMemberInGroupsRequestRequestTypeDef",
    "ListGroupMembershipsForMemberRequestRequestTypeDef",
    "CreateGroupMembershipResponseTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateUserResponseTypeDef",
    "DescribeGroupMembershipResponseTypeDef",
    "DescribeGroupResponseTypeDef",
    "GetGroupIdResponseTypeDef",
    "GetGroupMembershipIdResponseTypeDef",
    "GetUserIdResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "DescribeUserResponseTypeDef",
    "UserTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef",
    "ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListGroupsResponseTypeDef",
    "GetGroupIdRequestRequestTypeDef",
    "GetUserIdRequestRequestTypeDef",
    "IsMemberInGroupsResponseTypeDef",
    "ListGroupMembershipsForMemberResponseTypeDef",
    "ListGroupMembershipsResponseTypeDef",
    "ListUsersResponseTypeDef",
)

AddressTypeDef = TypedDict(
    "AddressTypeDef",
    {
        "StreetAddress": str,
        "Locality": str,
        "Region": str,
        "PostalCode": str,
        "Country": str,
        "Formatted": str,
        "Type": str,
        "Primary": bool,
    },
    total=False,
)

ExternalIdTypeDef = TypedDict(
    "ExternalIdTypeDef",
    {
        "Issuer": str,
        "Id": str,
    },
)

UniqueAttributeTypeDef = TypedDict(
    "UniqueAttributeTypeDef",
    {
        "AttributePath": str,
        "AttributeValue": Mapping[str, Any],
    },
)

_RequiredAttributeOperationTypeDef = TypedDict(
    "_RequiredAttributeOperationTypeDef",
    {
        "AttributePath": str,
    },
)
_OptionalAttributeOperationTypeDef = TypedDict(
    "_OptionalAttributeOperationTypeDef",
    {
        "AttributeValue": Mapping[str, Any],
    },
    total=False,
)

class AttributeOperationTypeDef(
    _RequiredAttributeOperationTypeDef, _OptionalAttributeOperationTypeDef
):
    pass

MemberIdTypeDef = TypedDict(
    "MemberIdTypeDef",
    {
        "UserId": str,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredCreateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGroupRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
    },
)
_OptionalCreateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGroupRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
    },
    total=False,
)

class CreateGroupRequestRequestTypeDef(
    _RequiredCreateGroupRequestRequestTypeDef, _OptionalCreateGroupRequestRequestTypeDef
):
    pass

EmailTypeDef = TypedDict(
    "EmailTypeDef",
    {
        "Value": str,
        "Type": str,
        "Primary": bool,
    },
    total=False,
)

NameTypeDef = TypedDict(
    "NameTypeDef",
    {
        "Formatted": str,
        "FamilyName": str,
        "GivenName": str,
        "MiddleName": str,
        "HonorificPrefix": str,
        "HonorificSuffix": str,
    },
    total=False,
)

PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef",
    {
        "Value": str,
        "Type": str,
        "Primary": bool,
    },
    total=False,
)

DeleteGroupMembershipRequestRequestTypeDef = TypedDict(
    "DeleteGroupMembershipRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "MembershipId": str,
    },
)

DeleteGroupRequestRequestTypeDef = TypedDict(
    "DeleteGroupRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "GroupId": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "UserId": str,
    },
)

DescribeGroupMembershipRequestRequestTypeDef = TypedDict(
    "DescribeGroupMembershipRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "MembershipId": str,
    },
)

DescribeGroupRequestRequestTypeDef = TypedDict(
    "DescribeGroupRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "GroupId": str,
    },
)

DescribeUserRequestRequestTypeDef = TypedDict(
    "DescribeUserRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "UserId": str,
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "AttributePath": str,
        "AttributeValue": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListGroupMembershipsRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupMembershipsRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "GroupId": str,
    },
)
_OptionalListGroupMembershipsRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupMembershipsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListGroupMembershipsRequestRequestTypeDef(
    _RequiredListGroupMembershipsRequestRequestTypeDef,
    _OptionalListGroupMembershipsRequestRequestTypeDef,
):
    pass

_RequiredGroupTypeDef = TypedDict(
    "_RequiredGroupTypeDef",
    {
        "GroupId": str,
        "IdentityStoreId": str,
    },
)
_OptionalGroupTypeDef = TypedDict(
    "_OptionalGroupTypeDef",
    {
        "DisplayName": str,
        "ExternalIds": List[ExternalIdTypeDef],
        "Description": str,
    },
    total=False,
)

class GroupTypeDef(_RequiredGroupTypeDef, _OptionalGroupTypeDef):
    pass

AlternateIdentifierTypeDef = TypedDict(
    "AlternateIdentifierTypeDef",
    {
        "ExternalId": ExternalIdTypeDef,
        "UniqueAttribute": UniqueAttributeTypeDef,
    },
    total=False,
)

UpdateGroupRequestRequestTypeDef = TypedDict(
    "UpdateGroupRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "GroupId": str,
        "Operations": Sequence[AttributeOperationTypeDef],
    },
)

UpdateUserRequestRequestTypeDef = TypedDict(
    "UpdateUserRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "UserId": str,
        "Operations": Sequence[AttributeOperationTypeDef],
    },
)

CreateGroupMembershipRequestRequestTypeDef = TypedDict(
    "CreateGroupMembershipRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "GroupId": str,
        "MemberId": MemberIdTypeDef,
    },
)

GetGroupMembershipIdRequestRequestTypeDef = TypedDict(
    "GetGroupMembershipIdRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "GroupId": str,
        "MemberId": MemberIdTypeDef,
    },
)

GroupMembershipExistenceResultTypeDef = TypedDict(
    "GroupMembershipExistenceResultTypeDef",
    {
        "GroupId": str,
        "MemberId": MemberIdTypeDef,
        "MembershipExists": bool,
    },
    total=False,
)

_RequiredGroupMembershipTypeDef = TypedDict(
    "_RequiredGroupMembershipTypeDef",
    {
        "IdentityStoreId": str,
    },
)
_OptionalGroupMembershipTypeDef = TypedDict(
    "_OptionalGroupMembershipTypeDef",
    {
        "MembershipId": str,
        "GroupId": str,
        "MemberId": MemberIdTypeDef,
    },
    total=False,
)

class GroupMembershipTypeDef(_RequiredGroupMembershipTypeDef, _OptionalGroupMembershipTypeDef):
    pass

IsMemberInGroupsRequestRequestTypeDef = TypedDict(
    "IsMemberInGroupsRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "MemberId": MemberIdTypeDef,
        "GroupIds": Sequence[str],
    },
)

_RequiredListGroupMembershipsForMemberRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupMembershipsForMemberRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "MemberId": MemberIdTypeDef,
    },
)
_OptionalListGroupMembershipsForMemberRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupMembershipsForMemberRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListGroupMembershipsForMemberRequestRequestTypeDef(
    _RequiredListGroupMembershipsForMemberRequestRequestTypeDef,
    _OptionalListGroupMembershipsForMemberRequestRequestTypeDef,
):
    pass

CreateGroupMembershipResponseTypeDef = TypedDict(
    "CreateGroupMembershipResponseTypeDef",
    {
        "MembershipId": str,
        "IdentityStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef",
    {
        "GroupId": str,
        "IdentityStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef",
    {
        "UserId": str,
        "IdentityStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupMembershipResponseTypeDef = TypedDict(
    "DescribeGroupMembershipResponseTypeDef",
    {
        "IdentityStoreId": str,
        "MembershipId": str,
        "GroupId": str,
        "MemberId": MemberIdTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupResponseTypeDef = TypedDict(
    "DescribeGroupResponseTypeDef",
    {
        "GroupId": str,
        "DisplayName": str,
        "ExternalIds": List[ExternalIdTypeDef],
        "Description": str,
        "IdentityStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupIdResponseTypeDef = TypedDict(
    "GetGroupIdResponseTypeDef",
    {
        "GroupId": str,
        "IdentityStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupMembershipIdResponseTypeDef = TypedDict(
    "GetGroupMembershipIdResponseTypeDef",
    {
        "MembershipId": str,
        "IdentityStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUserIdResponseTypeDef = TypedDict(
    "GetUserIdResponseTypeDef",
    {
        "UserId": str,
        "IdentityStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "UserName": str,
        "Name": NameTypeDef,
        "DisplayName": str,
        "NickName": str,
        "ProfileUrl": str,
        "Emails": Sequence[EmailTypeDef],
        "Addresses": Sequence[AddressTypeDef],
        "PhoneNumbers": Sequence[PhoneNumberTypeDef],
        "UserType": str,
        "Title": str,
        "PreferredLanguage": str,
        "Locale": str,
        "Timezone": str,
    },
    total=False,
)

class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "UserName": str,
        "UserId": str,
        "ExternalIds": List[ExternalIdTypeDef],
        "Name": NameTypeDef,
        "DisplayName": str,
        "NickName": str,
        "ProfileUrl": str,
        "Emails": List[EmailTypeDef],
        "Addresses": List[AddressTypeDef],
        "PhoneNumbers": List[PhoneNumberTypeDef],
        "UserType": str,
        "Title": str,
        "PreferredLanguage": str,
        "Locale": str,
        "Timezone": str,
        "IdentityStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUserTypeDef = TypedDict(
    "_RequiredUserTypeDef",
    {
        "UserId": str,
        "IdentityStoreId": str,
    },
)
_OptionalUserTypeDef = TypedDict(
    "_OptionalUserTypeDef",
    {
        "UserName": str,
        "ExternalIds": List[ExternalIdTypeDef],
        "Name": NameTypeDef,
        "DisplayName": str,
        "NickName": str,
        "ProfileUrl": str,
        "Emails": List[EmailTypeDef],
        "Addresses": List[AddressTypeDef],
        "PhoneNumbers": List[PhoneNumberTypeDef],
        "UserType": str,
        "Title": str,
        "PreferredLanguage": str,
        "Locale": str,
        "Timezone": str,
    },
    total=False,
)

class UserTypeDef(_RequiredUserTypeDef, _OptionalUserTypeDef):
    pass

_RequiredListGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupsRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
    },
)
_OptionalListGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

class ListGroupsRequestRequestTypeDef(
    _RequiredListGroupsRequestRequestTypeDef, _OptionalListGroupsRequestRequestTypeDef
):
    pass

_RequiredListUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListUsersRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
    },
)
_OptionalListUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListUsersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

class ListUsersRequestRequestTypeDef(
    _RequiredListUsersRequestRequestTypeDef, _OptionalListUsersRequestRequestTypeDef
):
    pass

_RequiredListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef = (
    TypedDict(
        "_RequiredListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef",
        {
            "IdentityStoreId": str,
            "MemberId": MemberIdTypeDef,
        },
    )
)
_OptionalListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef = (
    TypedDict(
        "_OptionalListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef",
        {
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

class ListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef(
    _RequiredListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef,
    _OptionalListGroupMembershipsForMemberRequestListGroupMembershipsForMemberPaginateTypeDef,
):
    pass

_RequiredListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef = TypedDict(
    "_RequiredListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef",
    {
        "IdentityStoreId": str,
        "GroupId": str,
    },
)
_OptionalListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef = TypedDict(
    "_OptionalListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef(
    _RequiredListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef,
    _OptionalListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef,
):
    pass

_RequiredListGroupsRequestListGroupsPaginateTypeDef = TypedDict(
    "_RequiredListGroupsRequestListGroupsPaginateTypeDef",
    {
        "IdentityStoreId": str,
    },
)
_OptionalListGroupsRequestListGroupsPaginateTypeDef = TypedDict(
    "_OptionalListGroupsRequestListGroupsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListGroupsRequestListGroupsPaginateTypeDef(
    _RequiredListGroupsRequestListGroupsPaginateTypeDef,
    _OptionalListGroupsRequestListGroupsPaginateTypeDef,
):
    pass

_RequiredListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "_RequiredListUsersRequestListUsersPaginateTypeDef",
    {
        "IdentityStoreId": str,
    },
)
_OptionalListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "_OptionalListUsersRequestListUsersPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListUsersRequestListUsersPaginateTypeDef(
    _RequiredListUsersRequestListUsersPaginateTypeDef,
    _OptionalListUsersRequestListUsersPaginateTypeDef,
):
    pass

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef",
    {
        "Groups": List[GroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGroupIdRequestRequestTypeDef = TypedDict(
    "GetGroupIdRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "AlternateIdentifier": AlternateIdentifierTypeDef,
    },
)

GetUserIdRequestRequestTypeDef = TypedDict(
    "GetUserIdRequestRequestTypeDef",
    {
        "IdentityStoreId": str,
        "AlternateIdentifier": AlternateIdentifierTypeDef,
    },
)

IsMemberInGroupsResponseTypeDef = TypedDict(
    "IsMemberInGroupsResponseTypeDef",
    {
        "Results": List[GroupMembershipExistenceResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupMembershipsForMemberResponseTypeDef = TypedDict(
    "ListGroupMembershipsForMemberResponseTypeDef",
    {
        "GroupMemberships": List[GroupMembershipTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupMembershipsResponseTypeDef = TypedDict(
    "ListGroupMembershipsResponseTypeDef",
    {
        "GroupMemberships": List[GroupMembershipTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "Users": List[UserTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
