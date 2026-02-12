from pydantic import BaseModel, Field


class AdviceBase(BaseModel):
    title: str = Field(..., description="Название совета")
    description: str = Field(..., description="Содержание совета")
    sort_order: int = Field(..., description="Порядок сортировки")
    is_active: bool = Field(default=True, description="Активен ли баннер")
