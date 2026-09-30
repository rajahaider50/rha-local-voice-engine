package com.rha.voiceengine

import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.Response
import java.io.File

/**
 * Unsigned Cloudinary upload client. Set the values from your Cloudinary account
 * in local.properties/BuildConfig before production release; never ship an API secret.
 */
class CloudinaryMediaClient(
    private val cloudName: String = BuildConfig.CLOUDINARY_CLOUD_NAME,
    private val uploadPreset: String = BuildConfig.CLOUDINARY_UPLOAD_PRESET,
    private val http: OkHttpClient = OkHttpClient()
) {
    fun upload(file: File, resourceType: String = "auto"): Response {
        require(cloudName.isNotBlank() && uploadPreset.isNotBlank()) { "Cloudinary is not configured" }
        val body = MultipartBody.Builder().setType(MultipartBody.FORM)
            .addFormDataPart("upload_preset", uploadPreset)
            .addFormDataPart("file", file.name, file.asRequestBody("application/octet-stream".toMediaType()))
            .build()
        return http.newCall(Request.Builder().url("https://api.cloudinary.com/v1_1/$cloudName/$resourceType/upload").post(body).build()).execute()
    }
}
