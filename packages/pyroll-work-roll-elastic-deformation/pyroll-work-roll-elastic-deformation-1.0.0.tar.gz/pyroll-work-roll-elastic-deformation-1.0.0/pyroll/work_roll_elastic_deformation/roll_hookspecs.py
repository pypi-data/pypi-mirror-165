from pyroll.core import Roll

if not hasattr(Roll.plugin_manager.hook, "youngs_modulus"):
    @Roll.hookspec
    def youngs_modulus(roll: Roll):
        """Elastic modulus of the roll material."""


@Roll.hookspec
def body(roll: Roll):
    """Body of the work roll."""
