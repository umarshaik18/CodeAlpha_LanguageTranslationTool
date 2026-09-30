from deep_translator import GoogleTranslator
import asyncio


class TranslationError(Exception):
    pass


class Translator:
    def __init__(self):
        self.supported_languages = {
            "en": "english",
            "te": "telugu",
            "hi": "hindi",
            "ta": "tamil",
            "es": "spanish",
        }

    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:

        if source_language == target_language:
            return text

        source = self.supported_languages.get(source_language)
        target = self.supported_languages.get(target_language)

        if not source:
            raise TranslationError(
                f"Unsupported source language: {source_language}"
            )

        if not target:
            raise TranslationError(
                f"Unsupported target language: {target_language}"
            )

        try:
            translated_text = await asyncio.to_thread(
                self._google_translate,
                text,
                source,
                target,
            )

            if not translated_text:
                raise TranslationError(
                    "Translation result was empty."
                )

            return translated_text.strip()

        except Exception as error:
            print(f"Google translation error: {error}")

            # Fallback to MyMemory
            try:
                translated_text = await asyncio.to_thread(
                    self._mymemory_translate,
                    text,
                    source_language,
                    target_language,
                )

                if not translated_text:
                    raise TranslationError(
                        "Translation result was empty."
                    )

                return translated_text.strip()

            except Exception as fallback_error:
                print(
                    f"MyMemory fallback error: {fallback_error}"
                )

                raise TranslationError(
                    "Translation service is temporarily unavailable. "
                    "Please try again."
                )

    @staticmethod
    def _google_translate(
        text: str,
        source: str,
        target: str,
    ) -> str:

        translator = GoogleTranslator(
            source=source,
            target=target,
        )

        return translator.translate(text)

    @staticmethod
    def _mymemory_translate(
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:

        import httpx

        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": (
                f"{source_language}|{target_language}"
            ),
        }

        response = httpx.get(
            url,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        return (
            data.get("responseData", {})
            .get("translatedText", "")
        )