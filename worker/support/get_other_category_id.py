def get_other_category_id(user_id, db_session):
    from infrastructure.database.models import Category

    category = (
        db_session.query(Category)
        .filter(Category.user_id == user_id)
        .filter(Category.name == "Outros")
        .first()
    )

    return category.id if category else None