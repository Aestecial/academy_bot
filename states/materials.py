from aiogram import Router, types
from keyboards.materials_keyboard import material_keyboard
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext

router = Router()

class Form():
    pass

@router.message(content_types=ContentType.TEXT, state=Form.waiting_for_text)
async def process_text_material(message: types.Message, state: FSMContext):
    choice = (await state.get_data()).get('choice')
    await message.answer(f"Текстовый материал: {message.text}")
    await state.finish()


@router.message(content_types=ContentType.PHOTO, state=Form.waiting_for_photo)
async def process_photo_material(message: types.Message, state: FSMContext):
    choice = (await state.get_data()).get('choice')
    photo_id = message.photo[-1].file_id
    await message.answer_photo(photo_id, caption=f"Фото: {choice}")
    await state.finish()


@router.message(content_types=ContentType.VIDEO, state=Form.waiting_for_video)
async def process_video_material(message: types.Message, state: FSMContext):
    choice = (await state.get_data()).get('choice')
    video_id = message.video.file_id
    await message.answer_video(video_id, caption=f"Видео: {choice}")
    await state.finish()


@router.message(content_types=ContentType.DOCUMENT, state=Form.waiting_for_file)
async def process_file_material(message: types.Message, state: FSMContext):
    choice = (await state.get_data()).get('choice')
    file_id = message.document.file_id
    await message.answer_document(file_id, caption=f"Файл: {choice}")
    await state.finish()


@router.message(lambda message: message.text.startswith('http'), state=Form.waiting_for_link)
async def process_link_material(message: types.Message, state: FSMContext):
    choice = (await state.get_data()).get('choice')
    await message.answer(f"Ссылка: {message.text}")
    await state.finish()