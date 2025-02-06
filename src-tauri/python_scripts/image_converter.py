from PIL import Image
import numpy as np
from ctypes import *
import tifffile
import os
import base64
from io import BytesIO
import time

# ICC profil yolları - Tauri kaynak yapısına göre
ICC_PROFILES_DIR = os.path.join(os.path.dirname(__file__), '..', 'resources', 'icc_profiles')
RGB_PROFILE = os.path.join(ICC_PROFILES_DIR, 'sRGB.icc')
CMYK_PROFILE = os.path.join(ICC_PROFILES_DIR, 'output_CMYK.icc')

# lcms2 kütüphanesini yükle (işletim sistemine göre)
if os.name == 'nt':  # Windows
    lcms2 = cdll.LoadLibrary('lcms2.dll')
else:  # Linux
    lcms2 = cdll.LoadLibrary('/lib/x86_64-linux-gnu/liblcms2.so')

# Fonksiyon dönüş tiplerini tanımla
lcms2.cmsOpenProfileFromFile.restype = c_void_p
lcms2.cmsCreateTransform.restype = c_void_p
lcms2.cmsDoTransform.restype = None
lcms2.cmsSaveProfileToMem.restype = c_bool

# lcms2 sabitleri
TYPE_RGB_16 = 0x4001a
TYPE_CMYK_16 = 0x60022
INTENT_PERCEPTUAL = 0

# Hata yönetimi için
ERROR_HANDLER_TYPE = CFUNCTYPE(None, c_void_p, c_uint32, c_char_p)

@ERROR_HANDLER_TYPE
def error_handler(contextID, errorcode, error_text):
    print(f"LCMS2 Error: {error_text.decode()}")

lcms2.cmsSetLogErrorHandler(error_handler)

# Argtype tanımlamaları
lcms2.cmsOpenProfileFromFile.argtypes = [c_char_p, c_char_p]
lcms2.cmsCreateTransform.argtypes = [c_void_p, c_uint32, c_void_p, c_uint32, c_uint32, c_uint32]
lcms2.cmsDoTransform.argtypes = [c_void_p, c_void_p, c_void_p, c_uint32]
lcms2.cmsSaveProfileToMem.argtypes = [c_void_p, c_void_p, POINTER(c_uint32)]
lcms2.cmsCloseProfile.argtypes = [c_void_p]
lcms2.cmsDeleteTransform.argtypes = [c_void_p]

class ImageColorConverter:
    def __init__(self):
        self.h_in_profile = None
        self.h_out_profile = None
        self.h_transform = None

    def initialize(self):
        try:
            print(f"Trying to load RGB profile from: {RGB_PROFILE}")
            print(f"Trying to load CMYK profile from: {CMYK_PROFILE}")
            
            if not os.path.exists(RGB_PROFILE):
                print(f"Directory contents of {os.path.dirname(RGB_PROFILE)}:")
                try:
                    print(os.listdir(os.path.dirname(RGB_PROFILE)))
                except Exception as e:
                    print(f"Could not list directory: {e}")
                return False, f"RGB profile file not found at {RGB_PROFILE}"
            
            if not os.path.exists(CMYK_PROFILE):
                return False, f"CMYK profile file not found at {CMYK_PROFILE}"

            self.h_in_profile = lcms2.cmsOpenProfileFromFile(RGB_PROFILE.encode(), b"r")
            if not self.h_in_profile:
                return False, "Failed to load RGB profile"

            self.h_out_profile = lcms2.cmsOpenProfileFromFile(CMYK_PROFILE.encode(), b"r")
            if not self.h_out_profile:
                return False, "Failed to load CMYK profile"

            self.h_transform = lcms2.cmsCreateTransform(
                c_void_p(self.h_in_profile),
                c_uint32(TYPE_RGB_16),
                c_void_p(self.h_out_profile),
                c_uint32(TYPE_CMYK_16),
                c_uint32(INTENT_PERCEPTUAL),
                c_uint32(0)
            )

            if not self.h_transform:
                return False, "Failed to create color transform"

            return True, "Initialization successful"

        except Exception as e:
            print(f"Initialize error: {str(e)}")
            self.cleanup()
            return False, f"Initialization failed: {str(e)}"

    def convert_image_from_base64(self, base64_image):
        try:
            # Base64 decode süresi
            decode_start = time.time()
            image_data = base64.b64decode(base64_image)
            decode_time = time.time() - decode_start
            print(f"Base64 decode süresi: {decode_time:.2f} saniye")

            # BytesIO ve Image.open süresi
            load_start = time.time()
            img = Image.open(BytesIO(image_data))
            load_time = time.time() - load_start
            print(f"Görüntü yükleme süresi: {load_time:.2f} saniye")
            
            # RGB dönüşüm ve numpy array oluşturma süresi
            convert_start = time.time()
            rgb_data = np.asarray(img.convert('RGB'), dtype=np.uint16) * 257
            rgb_data = np.ascontiguousarray(rgb_data)
            convert_time = time.time() - convert_start
            print(f"RGB dönüşüm süresi: {convert_time:.2f} saniye")
            
            width, height = img.size
            cmyk_data = np.zeros((height, width, 4), dtype=np.uint16, order='C')

            # CMYK dönüşüm süresi
            transform_start = time.time()
            lcms2.cmsDoTransform(
                self.h_transform,
                rgb_data.ctypes.data_as(c_void_p),
                cmyk_data.ctypes.data_as(c_void_p),
                width * height
            )
            transform_time = time.time() - transform_start
            print(f"CMYK dönüşüm süresi: {transform_time:.2f} saniye")

            # TIFF yazma süresi
            tiff_start = time.time()
            output_buffer = BytesIO()
            tifffile.imwrite(
                output_buffer,
                cmyk_data,
                photometric='SEPARATED',
                compression='zlib',
                compressionargs={'level': 5},
                resolution=(300, 300),
                metadata=None,
                predictor=True,
                tile=(256, 256),
                extratags=[(34675, 7, None, self._get_profile_data())]
            )
            tiff_time = time.time() - tiff_start
            print(f"TIFF yazma süresi: {tiff_time:.2f} saniye")

            # Base64 encode süresi
            encode_start = time.time()
            result = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
            encode_time = time.time() - encode_start
            print(f"Base64 encode süresi: {encode_time:.2f} saniye")

            # Toplam süre
            total_time = decode_time + load_time + convert_time + transform_time + tiff_time + encode_time
            print(f"\nToplam süre: {total_time:.2f} saniye")
            print(f"Base64 işlemleri toplam süresi: {decode_time + encode_time:.2f} saniye")
            print(f"Bellek işlemleri toplam süresi: {load_time + convert_time:.2f} saniye")

            return True, result

        except Exception as e:
            return False, str(e)

    def _get_profile_data(self):
        """ICC profil verisini cache'le"""
        if not hasattr(self, '_profile_data'):
            profile_size = c_uint32()
            lcms2.cmsSaveProfileToMem(self.h_out_profile, None, byref(profile_size))
            profile_buffer = create_string_buffer(profile_size.value)
            lcms2.cmsSaveProfileToMem(self.h_out_profile, profile_buffer, byref(profile_size))
            self._profile_data = bytes(profile_buffer.raw[:profile_size.value])
        return self._profile_data

    def cleanup(self):
        if self.h_transform:
            lcms2.cmsDeleteTransform(c_void_p(self.h_transform))
        if self.h_in_profile:
            lcms2.cmsCloseProfile(c_void_p(self.h_in_profile))
        if self.h_out_profile:
            lcms2.cmsCloseProfile(c_void_p(self.h_out_profile))
        self.h_transform = None
        self.h_in_profile = None
        self.h_out_profile = None

    def __del__(self):
        self.cleanup()

def convert_png_to_cmyk(base64_png):
    """
    Rust'tan çağrılacak ana fonksiyon
    Args:
        base64_png: Base64 formatında PNG görüntü verisi
    Returns:
        (success, result): (bool, str) tuple
        success: İşlemin başarı durumu
        result: Başarılı ise base64 TIFF verisi, başarısız ise hata mesajı
    """
    converter = ImageColorConverter()
    
    success, message = converter.initialize()
    if not success:
        return False, message

    success, result = converter.convert_image_from_base64(base64_png)
    converter.cleanup()
    
    return success, result 