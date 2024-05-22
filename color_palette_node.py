from invokeai.invocation_api import (
    invocation,
    BaseInvocation,
    InputField,
    InvocationContext,
    ImageField,
    ImageOutput,
    ColorField,
    Input,
)
from typing import List, Optional
from PIL import Image, ImageFilter

@invocation(
    "color_palette",
    title="Color Palette",
    tags=["color", "palette", "color palette"],
    category="color",
    version="1.0.0",
)
class ColorPaletteInvocation(BaseInvocation):
    """
    This node generates a color palette image from a list of ColorField inputs.
    """
    colors: List[ColorField] = InputField(description="List of colors to include in the palette", ui_order=0, input=Input.Connection,)
    image_size: int = InputField(default=1024, description="Size of the output image", ui_order=1)
    blending: int = InputField(default=0, description="Blending the edges together for more variation", ui_order=2)

    def invoke(self, context: InvocationContext) -> ImageOutput:
        """
        Generate a color palette image from a list of ColorField inputs.
        """

        image = Image.new("RGB", (self.image_size, self.image_size))
        color_width = self.image_size // len(self.colors)
        for i, color in enumerate(self.colors):
            for x in range(color_width):
                for y in range(self.image_size):
                    pixel_value = color.tuple()[:3]
                    image.putpixel((i * color_width + x, y), pixel_value)
        if self.blending > 0:
            image = image.filter(ImageFilter.GaussianBlur(self.blending))
        image_dto = context.images.save(image)
        return ImageOutput.build(image_dto)