from .decorators import permission_required


class PermissionRequiredMixin:
    """
    This mixin is available in Django >=1.9; emulate it in <1.9
    """
    permission_required = tuple()

    @classmethod
    def as_view(cls, **kwargs):
        restrict = permission_required(cls.permission_required)
        view = super(PermissionRequiredMixin, cls).as_view(**kwargs)
        return restrict(view)
