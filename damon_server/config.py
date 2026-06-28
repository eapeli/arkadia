"""
Damon Server - Configuration
"""
from __future__ import annotations

import os
import secrets
from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "Damon Agent API"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"  # development, staging, production
    api_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/damon",
        description="PostgreSQL async connection URL",
    )
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_pool_pre_ping: bool = True

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )
    redis_max_connections: int = 50

    # Security
    secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Secret key for JWT signing",
    )
    encryption_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Encryption key for sensitive data",
    )
    jwt_algorithm: str = "RS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    jwt_issuer: str = "damon-agent"
    jwt_audience: str = "damon-agent-api"

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "tauri://localhost"],
        description="Allowed CORS origins",
    )
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_default: str = "100/minute"
    rate_limit_auth: str = "20/minute"
    rate_limit_webhook: str = "1000/minute"

    # License Server
    license_server_url: str = "https://license.damon-agent.dev"
    license_server_enabled: bool = True

    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""

    # WebSocket
    ws_heartbeat_interval: int = 30
    ws_max_connections: int = 10000

    # Monitoring
    prometheus_enabled: bool = True
    prometheus_port: int = 9090

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json, console
    log_file: Optional[str] = None

    # File Storage
    upload_dir: str = "./uploads"
    max_upload_size: int = 100 * 1024 * 1024  # 100MB

    # Email (for notifications)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@damon-agent.dev"

    # Feature Flags
    feature_license_enforcement: bool = True
    feature_usage_tracking: bool = True
    feature_audit_logs: bool = True
    feature_team_workspaces: bool = True

    # Agent Integration
    agent_socket_path: str = "/tmp/damon_agent.sock"
    agent_command_timeout: int = 300

    # Admin
    admin_api_key: str = ""

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()