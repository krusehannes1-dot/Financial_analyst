"""
Pydantic Models for Request and Response validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class AnalyzeRequest(BaseModel):
    """
    Request model for the /analyze endpoint.
    """
    isin: str = Field(
        ...,
        description="International Securities Identification Number (ISIN)",
        min_length=12,
        max_length=12,
        examples=["US0378331005"]
    )
    asset_name: Optional[str] = Field(
        None,
        description="Optional asset name for reference",
        examples=["Apple Inc."]
    )

    @validator("isin")
    def validate_isin_format(cls, v):
        """Validate ISIN format (basic check)."""
        v = v.strip().upper()

        if len(v) != 12:
            raise ValueError("ISIN must be exactly 12 characters")

        if not v[:2].isalpha():
            raise ValueError("ISIN must start with 2-letter country code")

        if not v[2:].isalnum():
            raise ValueError("ISIN must contain only alphanumeric characters after country code")

        return v


class AnalyzeResponse(BaseModel):
    """
    Response model for the /analyze endpoint.
    """
    success: bool = Field(
        ...,
        description="Whether the analysis was successful"
    )
    ticker: str = Field(
        ...,
        description="Stock ticker symbol used for analysis"
    )
    isin: str = Field(
        ...,
        description="ISIN that was analyzed"
    )
    report: str = Field(
        ...,
        description="Markdown-formatted investment report"
    )
    metadata: Optional[dict] = Field(
        None,
        description="Additional metadata about the analysis"
    )


class ErrorResponse(BaseModel):
    """
    Error response model.
    """
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


class HealthCheckResponse(BaseModel):
    """
    Health check response model.
    """
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="API version")


class AdviseRequest(BaseModel):
    """
    Request model for the /advise endpoint (Trading Advisory).
    """
    isin: str = Field(
        ...,
        description="International Securities Identification Number (ISIN)",
        min_length=12,
        max_length=12,
        examples=["US67066G1040"]
    )
    asset_name: Optional[str] = Field(
        None,
        description="Optional asset name for reference",
        examples=["NVIDIA Corporation"]
    )

    @validator("isin")
    def validate_isin_format(cls, v):
        """Validate ISIN format (basic check)."""
        v = v.strip().upper()

        if len(v) != 12:
            raise ValueError("ISIN must be exactly 12 characters")

        if not v[:2].isalpha():
            raise ValueError("ISIN must start with 2-letter country code")

        if not v[2:].isalnum():
            raise ValueError("ISIN must contain only alphanumeric characters after country code")

        return v


class AdviseResponse(BaseModel):
    """
    Response model for the /advise endpoint (Trading Advisory).
    """
    success: bool = Field(
        ...,
        description="Whether the advisory was successful"
    )
    ticker: str = Field(
        ...,
        description="Stock ticker symbol used for advisory"
    )
    isin: str = Field(
        ...,
        description="ISIN that was analyzed"
    )
    advisory_report: str = Field(
        ...,
        description="Markdown-formatted trading advisory with action card"
    )
    technical_data: Optional[dict] = Field(
        None,
        description="Key technical indicators used in the analysis"
    )
    metadata: Optional[dict] = Field(
        None,
        description="Additional metadata about the advisory"
    )
