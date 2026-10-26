import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for geometric shapes."""

    @abstractmethod
    def area(self) -> int | float:
        """Return the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self) -> int | float:
        """Return the perimeter of the shape."""
        pass

    @staticmethod
    def _check_positive(value: int | float, name: str) -> int | float:
        """Validate that a dimension is a positive number."""
        if value <= 0:
            raise ValueError(f"{name} must be positive")
        return value

    def __str__(self) -> str:
        """Return a human-readable representation of the shape."""
        return f"{type(self).__name__}: S = {self.area():.2f}, P = {self.perimeter():.2f}"


class Rectangle(Shape):
    """A rectangle defined by length and width."""

    def __init__(self, length: int | float, width: int | float) -> None:
        """Initialize a rectangle with length and width."""
        self.length = length
        self.width = width

    @property
    def length(self) -> int | float:
        """Get the length of the rectangle."""
        return self._length

    @length.setter
    def length(self, value: int | float) -> None:
        self._length = self._check_positive(value, "Length")

    @property
    def width(self) -> int | float:
        """Get the width of the rectangle."""
        return self._width

    @width.setter
    def width(self, value: int | float) -> None:
        self._width = self._check_positive(value, "Width")

    def area(self) -> int | float:
        """Calculate and return the area of the rectangle."""
        return self._length * self._width

    def perimeter(self) -> int | float:
        """Calculate and return the perimeter of the rectangle."""
        return 2 * (self._length + self._width)


class Square(Rectangle):
    """A square: a rectangle with equal sides."""

    def __init__(self, side: int | float) -> None:
        """Initialize a square with side."""
        super().__init__(side, side)

    @property
    def side(self) -> int | float:
        """Get the side of the square."""
        return self._length

    @side.setter
    def side(self, value: int | float) -> None:
        self._length = self._width = self._check_positive(value, "Side")


class Circle(Shape):
    """A circle defined by its radius."""

    def __init__(self, radius: int | float) -> None:
        """Initialize a circle with radius."""
        self.radius = radius

    @property
    def radius(self) -> int | float:
        """Get the radius of the circle."""
        return self._radius

    @radius.setter
    def radius(self, value: int | float) -> None:
        self._radius = self._check_positive(value, "Radius")

    def area(self) -> float:
        """Calculate and return the area of the circle."""
        return math.pi * self._radius**2

    def perimeter(self) -> float:
        """Calculate and return the perimeter of the circle."""
        return 2 * math.pi * self._radius


if __name__ == "__main__":
    shapes: list[Shape] = [Rectangle(5, 3), Square(4), Circle(1)]
    for s in shapes:
        print(s)
    # Rectangle: area=15.00, perimeter=16.00
    # Square: area=16.00, perimeter=16.00
    # Circle: area=3.14, perimeter=6.28
