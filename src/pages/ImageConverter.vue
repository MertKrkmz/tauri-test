<template>
	<div class="p-4 max-w-2xl mx-auto">
		<div class="mb-4">
			<input
				type="file"
				ref="fileInput"
				@change="handleFileSelect"
				accept="image/*"
				class="hidden"
			/>
			<button
				@click="$refs.fileInput.click()"
				class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
			>
				Görüntü Seç
			</button>
		</div>

		<!-- Seçilen görüntü önizleme -->
		<div v-if="selectedImage" class="mb-4">
			<h3 class="text-lg font-semibold mb-2">Seçilen Görüntü:</h3>
			<img
				:src="selectedImage"
				alt="Selected"
				class="max-w-full h-auto border rounded"
			/>
		</div>

		<!-- Dönüştürme ve İndirme butonları -->
		<div class="mb-4">
			<button
				@click="handleConvert"
				:disabled="!selectedImage || isLoading"
				:class="`bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded mr-2 
					${(!selectedImage || isLoading) ? 'opacity-50 cursor-not-allowed' : ''}`"
			>
				{{ isLoading ? 'Dönüştürülüyor...' : "CMYK'ya Dönüştür" }}
			</button>

			<button
				v-if="convertedImage"
				@click="handleDownload"
				class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded"
			>
				TIFF Olarak İndir
			</button>
		</div>

		<!-- Hata mesajı -->
		<div v-if="error" class="text-red-500 mb-4">
			{{ error }}
		</div>

		<!-- Başarı mesajı -->
		<div v-if="convertedImage" class="text-green-500 mb-4">
			Görüntü başarıyla CMYK'ya dönüştürüldü!
			<div v-if="convertTime" class="text-sm mt-1">
				Dönüştürme süresi: {{ convertTime }} saniye
			</div>
		</div>

		<!-- Dönüştürme süresi -->
		<div v-if="convertTime" class="text-gray-500 mb-4">
			Dönüştürme süresi: {{ convertTime }} saniye
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { invoke } from '@tauri-apps/api/core'

const fileInput = ref<HTMLInputElement | null>(null)
const selectedImage = ref<string | null>(null)
const convertedImage = ref<string | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)
const convertTime = ref<number | null>(null)

const handleFileSelect = (event: Event) => {
	const target = event.target as HTMLInputElement
	const file = target.files?.[0]
	
	if (file) {
		if (!file.type.startsWith('image/')) {
			error.value = 'Lütfen geçerli bir görüntü dosyası seçin'
			return
		}

		const reader = new FileReader()
		reader.onload = (e) => {
			const base64 = e.target?.result as string
			selectedImage.value = base64
			convertedImage.value = null
			error.value = null
		}
		reader.readAsDataURL(file)
	}
}

const handleConvert = async () => {
	if (!selectedImage.value) {
		error.value = 'Lütfen önce bir görüntü seçin'
		return
	}

	isLoading.value = true
	error.value = null
	
	try {
		const base64Data = selectedImage.value.split(',')[1]
		const startTime = performance.now()
		const result = await invoke<string>('convert_png_to_cmyk', {
			imageData: base64Data
		})
		convertedImage.value = result
		const endTime = performance.now()
		convertTime.value = Number(((endTime - startTime) / 1000).toFixed(2))
	} catch (err) {
		error.value = `Dönüştürme hatası: ${err}`
	} finally {
		isLoading.value = false
	}
}

const handleDownload = () => {
	if (!convertedImage.value) return

	const binary = atob(convertedImage.value)
	const bytes = new Uint8Array(binary.length)
	for (let i = 0; i < binary.length; i++) {
		bytes[i] = binary.charCodeAt(i)
	}

	const blob = new Blob([bytes], { type: 'image/tiff' })
	const url = URL.createObjectURL(blob)
	
	const a = document.createElement('a')
	a.href = url
	a.download = 'converted_image.tiff'
	document.body.appendChild(a)
	a.click()
	document.body.removeChild(a)
	URL.revokeObjectURL(url)
}
</script> 