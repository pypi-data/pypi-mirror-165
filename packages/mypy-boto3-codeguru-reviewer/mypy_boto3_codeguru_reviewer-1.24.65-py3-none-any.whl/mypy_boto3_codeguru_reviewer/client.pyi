"""
Type annotations for codeguru-reviewer service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codeguru_reviewer.client import CodeGuruReviewerClient

    session = Session()
    client: CodeGuruReviewerClient = session.client("codeguru-reviewer")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    JobStateType,
    ProviderTypeType,
    ReactionType,
    RepositoryAssociationStateType,
    TypeType,
)
from .paginator import ListRepositoryAssociationsPaginator
from .type_defs import (
    AssociateRepositoryResponseTypeDef,
    CodeReviewTypeTypeDef,
    CreateCodeReviewResponseTypeDef,
    DescribeCodeReviewResponseTypeDef,
    DescribeRecommendationFeedbackResponseTypeDef,
    DescribeRepositoryAssociationResponseTypeDef,
    DisassociateRepositoryResponseTypeDef,
    KMSKeyDetailsTypeDef,
    ListCodeReviewsResponseTypeDef,
    ListRecommendationFeedbackResponseTypeDef,
    ListRecommendationsResponseTypeDef,
    ListRepositoryAssociationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    RepositoryTypeDef,
)
from .waiter import CodeReviewCompletedWaiter, RepositoryAssociationSucceededWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CodeGuruReviewerClient",)

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
    NotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CodeGuruReviewerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeGuruReviewerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#exceptions)
        """
    def associate_repository(
        self,
        *,
        Repository: RepositoryTypeDef,
        ClientRequestToken: str = ...,
        Tags: Mapping[str, str] = ...,
        KMSKeyDetails: KMSKeyDetailsTypeDef = ...
    ) -> AssociateRepositoryResponseTypeDef:
        """
        Use to associate an Amazon Web Services CodeCommit repository or a repository
        managed by Amazon Web Services CodeStar Connections with Amazon CodeGuru
        Reviewer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.associate_repository)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#associate_repository)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#can_paginate)
        """
    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#close)
        """
    def create_code_review(
        self,
        *,
        Name: str,
        RepositoryAssociationArn: str,
        Type: CodeReviewTypeTypeDef,
        ClientRequestToken: str = ...
    ) -> CreateCodeReviewResponseTypeDef:
        """
        Use to create a code review with a
        [CodeReviewType](https://docs.aws.amazon.com/codeguru/latest/reviewer-
        api/API_CodeReviewType.html)_ of `RepositoryAnalysis`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.create_code_review)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#create_code_review)
        """
    def describe_code_review(self, *, CodeReviewArn: str) -> DescribeCodeReviewResponseTypeDef:
        """
        Returns the metadata associated with the code review along with its status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.describe_code_review)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#describe_code_review)
        """
    def describe_recommendation_feedback(
        self, *, CodeReviewArn: str, RecommendationId: str, UserId: str = ...
    ) -> DescribeRecommendationFeedbackResponseTypeDef:
        """
        Describes the customer feedback for a CodeGuru Reviewer recommendation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.describe_recommendation_feedback)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#describe_recommendation_feedback)
        """
    def describe_repository_association(
        self, *, AssociationArn: str
    ) -> DescribeRepositoryAssociationResponseTypeDef:
        """
        Returns a
        [RepositoryAssociation](https://docs.aws.amazon.com/codeguru/latest/reviewer-
        api/API_RepositoryAssociation.html)_ object that contains information about the
        requested repository association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.describe_repository_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#describe_repository_association)
        """
    def disassociate_repository(
        self, *, AssociationArn: str
    ) -> DisassociateRepositoryResponseTypeDef:
        """
        Removes the association between Amazon CodeGuru Reviewer and a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.disassociate_repository)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#disassociate_repository)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#generate_presigned_url)
        """
    def list_code_reviews(
        self,
        *,
        Type: TypeType,
        ProviderTypes: Sequence[ProviderTypeType] = ...,
        States: Sequence[JobStateType] = ...,
        RepositoryNames: Sequence[str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListCodeReviewsResponseTypeDef:
        """
        Lists all the code reviews that the customer has created in the past 90 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.list_code_reviews)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#list_code_reviews)
        """
    def list_recommendation_feedback(
        self,
        *,
        CodeReviewArn: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        UserIds: Sequence[str] = ...,
        RecommendationIds: Sequence[str] = ...
    ) -> ListRecommendationFeedbackResponseTypeDef:
        """
        Returns a list of
        [RecommendationFeedbackSummary](https://docs.aws.amazon.com/codeguru/latest/reviewer-
        api/API_RecommendationFeedbackSummary.html)_ objects that contain customer
        recommendation feedback for all CodeGuru Reviewer users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.list_recommendation_feedback)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#list_recommendation_feedback)
        """
    def list_recommendations(
        self, *, CodeReviewArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListRecommendationsResponseTypeDef:
        """
        Returns the list of all recommendations for a completed code review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.list_recommendations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#list_recommendations)
        """
    def list_repository_associations(
        self,
        *,
        ProviderTypes: Sequence[ProviderTypeType] = ...,
        States: Sequence[RepositoryAssociationStateType] = ...,
        Names: Sequence[str] = ...,
        Owners: Sequence[str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListRepositoryAssociationsResponseTypeDef:
        """
        Returns a list of
        [RepositoryAssociationSummary](https://docs.aws.amazon.com/codeguru/latest/reviewer-
        api/API_RepositoryAssociationSummary.html)_ objects that contain summary
        information about a repository association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.list_repository_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#list_repository_associations)
        """
    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the list of tags associated with an associated repository resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#list_tags_for_resource)
        """
    def put_recommendation_feedback(
        self, *, CodeReviewArn: str, RecommendationId: str, Reactions: Sequence[ReactionType]
    ) -> Dict[str, Any]:
        """
        Stores customer feedback for a CodeGuru Reviewer recommendation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.put_recommendation_feedback)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#put_recommendation_feedback)
        """
    def tag_resource(self, *, resourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds one or more tags to an associated repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#tag_resource)
        """
    def untag_resource(self, *, resourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from an associated repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#untag_resource)
        """
    def get_paginator(
        self, operation_name: Literal["list_repository_associations"]
    ) -> ListRepositoryAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#get_paginator)
        """
    @overload
    def get_waiter(
        self, waiter_name: Literal["code_review_completed"]
    ) -> CodeReviewCompletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#get_waiter)
        """
    @overload
    def get_waiter(
        self, waiter_name: Literal["repository_association_succeeded"]
    ) -> RepositoryAssociationSucceededWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/client/#get_waiter)
        """
