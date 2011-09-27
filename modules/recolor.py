"""Can compile a vertical Saturation, Value, Alpha"""

from pygame import image, surfarray, Surface, SRCALPHA, BLEND_MULT, BLEND_RGB_SUB

def compileSVASheet(sheet, color):
    color = tuple([255-c for c in color])
    
    width = sheet.get_width()
    height = sheet.get_height() / 3
    
    colorSurf = Surface((width, height))
    colorSurf.fill(color)
    
    colorSurf.blit(sheet, (0, 0), None, BLEND_MULT)
    
    # Now create a white surface so we can invert the Saturation map
    result = Surface((width, height), SRCALPHA)
    result.fill((255, 255, 255))
    
    result.blit(colorSurf, (0, 0), None, BLEND_RGB_SUB)
    
    # Multiply this with the Value Map
    result.blit(sheet, (0, -height), None, BLEND_MULT)
    
    # copy the alpha mask from the spritesheet
    alpha = Surface((width, height))
    alpha.blit(sheet, (0, -2 * height))
    
    #convert the (nearly done) Surface to per pixel alpha
    result.convert_alpha()
    
    # Use Numpy here
    numWhite = surfarray.pixels_alpha( result )
    
    numAlpha = surfarray.pixels3d( alpha )
    
    numWhite[ :, : ] = numAlpha[ :, :, 0 ]
    
    return result.copy()