from deprecated.classic import ClassicAdapter
from deprecated import deprecated



class ClassicAdapterNoDefaultMessage(ClassicAdapter):
    def get_deprecated_msg(self, *args, **kwargs):
        return self.reason



def renamed_function( fun, old_name="" ):
    """Copy the function and emit a deprecation warning


    Parameters
    ----------
    fun : fun
        The new function
    old_name : str, optional
        The name of the old function. The default is "".

    Returns
    -------
    fun
        The decorated function

    Example
    -------

    >>> test_old = renamed_function(test_new, "test_old")
    >>> test_old()
    DeprecationWarning: test_old has been renamed test_new

    """
    return deprecated( fun, reason = f"{old_name:} has been renamed {fun.__name__:}" , adapter_cls = ClassicAdapterNoDefaultMessage)



if __name__ == "__main__":

    def test_new():
        return "1"

    test_old = renamed_function(test_new, "test_old")
    test_old()


    class TestClass():
        def new_method_name(self, i) :
            print (i)

    TestClass.oldMethodName = renamed_function(TestClass.new_method_name, "oldMethodName")

    a = TestClass()
    a.oldMethodName(2)




