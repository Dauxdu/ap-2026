class Rectangle:
    """A class representing a rectangle."""

    def __init__(self, length: int | float, width: int | float) -> None:
        """Initialize a rectangle with length and width."""
        self.length = length
        self.width = width

    def __str__(self) -> str:
        """Return a human-readable representation of the rectangle."""
        return f"{self.__length} x {self.__width})"

    @property
    def length(self) -> int | float:
        """Get the length of the rectangle."""
        return self.__length

    @length.setter
    def length(self, value: int | float) -> None:
        """Set the length of the rectangle."""
        if value <= 0:
            raise ValueError("Length must be positive")
        self.__length = value

    @property
    def width(self) -> int | float:
        """Get the width of the rectangle."""
        return self.__width

    @width.setter
    def width(self, value: int | float) -> None:
        """Set the width of the rectangle."""
        if value <= 0:
            raise ValueError("Width must be positive")
        self.__width = value

    def area(self) -> int | float:
        """Calculate and return the area of the rectangle."""
        return self.__length * self.__width

    def perimeter(self) -> int | float:
        """Calculate and return the perimeter of the rectangle."""
        return 2 * (self.__length + self.__width)

    def is_square(self) -> bool:
        """Check if the rectangle is a square."""
        return self.__length == self.__width


if __name__ == "__main__":
    r = Rectangle(5, 3)

    print(r.area())  # 15
    print(r.perimeter())  # 16
    print(r.is_square())  # False
    r.width = 5
    print(r.is_square())  # True
    print(r)
