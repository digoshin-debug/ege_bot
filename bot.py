import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Твой рабочий токен
API_TOKEN = '8483502683:AAFrePOO106No_8wy71QsCr7OyhJdrM2f-o'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База из 15 вопросов с обновленными понятными формулировками заданий
QUESTIONS = [
    {
        "text": "⚡️ Вопрос 1 из 15 (Задание 9 в ЕГЭ)\n\nВ каком слове на месте пропуска пишется буква О?",
        "answers": ["заг..релый", "прик..снуться"],
        "correct_index": 1,
        "topic": "орфография"
    },
    {
        "text": "⚡️ Вопрос 2 из 15 (Задание 10 в ЕГЭ)\n\nВ каком варианте ПРАВИЛЬНО вставлена буква?",
        "answers": ["безынициативный", "сверхыинтересный"],
        "correct_index": 0,
        "topic": "орфография"
    },
    {
        "text": "⚡️ Вопрос 3 из 15 (Задание 11 в ЕГЭ)\n\nВыберите вариант без ошибки:",
        "answers": ["вытереть досухо", "вытереть досуха"],
        "correct_index": 1,
        "topic": "орфография"
    },
    {
        "text": "⚡️ Вопрос 4 из 15 (Задание 12 в ЕГЭ)\n\nКак правильно?",
        "answers": ["они клеят коробку", "они клеют коробку"],
        "correct_index": 0,
        "topic": "орфография"
    },
    {
        "text": "⚡️ Вопрос 5 из 15 (Задание 13 в ЕГЭ)\n\nОпределите слитное написание НЕ:",
        "answers": ["(Не)смотря на ливень, мы пошли", "(Не)смотря по сторонам, он бежал"],
        "correct_index": 0,
        "topic": "орфография"
    },
    {
        "text": "⚡️ Вопрос 6 из 15 (Задание 14 в ЕГЭ)\n\nКак пишется выделенное наречие: «Он уменьшил расходы (В)ПОЛОВИНУ»?",
        "answers": ["Слитно", "Раздельно"],
        "correct_index": 0,
        "topic": "орфография"
    },
    {
        "text": "⚡️ Вопрос 7 из 15 (Задание 15 в ЕГЭ)\n\nСколько букв Н пишется в слове: «жаре...ая на масле рыба»?",
        "answers": ["Одна (Н)", "Две (НН)"],
        "correct_index": 1,
        "topic": "орфография"
    },
    {
        "text": "⚡️ Вопрос 8 из 15 (Задание 16 в ЕГЭ)\n\nНужна ли запятая перед союзом И: «В лесу было тихо и пахло сыростью»?",
        "answers": ["Да, нужна", "Нет, не нужна"],
        "correct_index": 1,
        "topic": "пунктуация"
    },
    {
        "text": "⚡️ Вопрос 9 из 15 (Задание 17 в ЕГЭ)\n\nВ каком предложении НЕ НУЖНЫ запятые?",
        "answers": ["Книга лежащая на столе была открыта.", "Лежащая на столе книга была открыта."],
        "correct_index": 1,
        "topic": "пунктуация"
    },
    {
        "text": "⚡️ Вопрос 10 из 15 (Задание 18 в ЕГЭ)\n\nВыделяется ли слово «ОДНАКО» запятой в начале этого предложения: «Однако мы решили остаться»?",
        "answers": ["Да", "Нет"],
        "correct_index": 1,
        "topic": "пунктуация"
    },
    {
        "text": "⚡️ Вопрос 11 из 15 (Задание 19 в ЕГЭ)\n\nГде должна стоять запятая: «Мы вышли к поляне (1) на краю (2) которой (3) рос дуб»?",
        "answers": ["На месте (1)", "На месте (2)", "На месте (3)"],
        "correct_index": 0,
        "topic": "пунктуация"
    },
    {
        "text": "⚡️ Вопрос 12 из 15 (Задание 20 в ЕГЭ)\n\nНужна ли запятая на месте пропуска: «Он сказал, что уезжает, и (_) если мы хотим попрощаться, надо поторопиться»?",
        "answers": ["Да, нужна", "Нет, не нужна"],
        "correct_index": 0,
        "topic": "пунктуация"
    },
    {
        "text": "⚡️ Вопрос 13 из 15 (Задание 21 в ЕГЭ)\n\nМожно ли объединить эти два предложения в один answer по правилу «Тире между подлежащим и сказуемым»: 1) «Москва — столица» и 2) «Сыр выпал — с ним была плутовка такова»?",
        "answers": ["Да", "Нет"],
        "correct_index": 1,
        "topic": "пунктуация"
    },
    {
        "text": "⚡️ Вопрос 14 из 15 (Задание 7 в ЕГЭ)\n\nВыберите грамматически верную форму родительного падежа:",
        "answers": ["пять кочерёгов, пара туфлей", "пять кочерёг, пара туфель"],
        "correct_index": 1,
        "topic": "грамматика"
    },
    {
        "text": "⚡️ Вопрос 15 из 15 (Задание 26 в ЕГЭ)\n\nКак называется приём, когда одинаковые слова повторяются в начале соседних предложений?",
        "answers": ["Анафора", "Эпифора"],
        "correct_index": 0,
        "topic": "грамматика"
    }
]

user_data = {}

def get_quiz_keyboard(question_index: int):
    builder = InlineKeyboardBuilder()
    q = QUESTIONS[question_index]
    for idx, answer in enumerate(q["answers"]):
        builder.button(text=answer, callback_data=f"quiz_{question_index}_{idx}")
    builder.adjust(1)
    return builder.as_markup()

# 1. Обновленное приветственное сообщение со смайликами
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {"current_question": 0, "score": 0, "wrong_topics": set()}
    
    start_keyboard = InlineKeyboardBuilder()
    start_keyboard.button(text="🚀 Начать диагностику", callback_data="start_test")
    
    await message.answer(
        "👋 Привет! Добро пожаловать на экспресс-диагностику ЕГЭ по русскому языку от Step by Step.\n\n"
        "🛑 Во время теста мы не показываем правильные ответы, чтобы не сбивать фокус. В конце ты увидишь свой балл, "
        "разбор ошибок и сможешь записаться на индивидуальную диагностику с преподавателем. На ней вы подробно "
        "разберете задания и составите план подготовки к целевому результату.\n\n"
        "💡 Важно: экспресс-диагностика не заменяет полноценную диагностику с разбором всех заданий. "
        "Она помогает быстро определить твой уровень и подсветить основные пробелы.\n\n"
        "👇 Нажми кнопку ниже — тест займет всего 1,5 минуты. Удачи!",
        reply_markup=start_keyboard.as_markup()
    )

@dp.callback_query(F.data == "start_test")
async def start_quiz_workflow(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"current_question": 0, "score": 0, "wrong_topics": set()}
        
    await callback.message.edit_text(
        text=QUESTIONS[0]['text'],
        reply_markup=get_quiz_keyboard(0)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("quiz_"))
async def handle_quiz_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"current_question": 0, "score": 0, "wrong_topics": set()}

    _, q_idx, answer_idx = callback.data.split("_")
    q_idx = int(q_idx)
    answer_idx = int(answer_idx)

    if answer_idx == QUESTIONS[q_idx]["correct_index"]:
        user_data[user_id]["score"] += 1
    else:
        user_data[user_id]["wrong_topics"].add(QUESTIONS[q_idx]["topic"])

    next_q_idx = q_idx + 1

    if next_q_idx < len(QUESTIONS):
        user_data[user_id]["current_question"] = next_q_idx
        await callback.message.edit_text(
            text=QUESTIONS[next_q_idx]["text"],
            reply_markup=get_quiz_keyboard(next_q_idx)
        )
    else:
        score = user_data[user_id]["score"]
        total = len(QUESTIONS)
        wrong_topics = user_data[user_id]["wrong_topics"]
        
        # 4. Раскрыли номера заданий, добавив расшифровку тем
        why_text = ""
        if "орфография" in wrong_topics:
            why_text += (
                "📍 В блоке «Орфография» (задания 9–15 в ЕГЭ: корни, приставки, суффиксы, окончания глаголов, "
                "слитное/раздельное написание НЕ и слов, а также Н/НН) сейчас во многом идет опора на интуицию, а не на алгоритмы. "
                "Составители экзамена усложнили правила, поэтому из-за незнания тонких исключений здесь легко теряются ключевые баллы.\n\n"
            )
        if "пунктуация" in wrong_topics:
            why_text += (
                "📍 В блоке «Пунктуация» (задания 16–21 в ЕГЭ: знаки препинания в сложных предложениях, при причастных/деепричастных "
                "оборотах, вводных словах, а также задание на стык союзов и пунктуационный анализ текста) слабым местом оказались самые хитрые правила. "
                "Без твердых алгоритмов здесь легко потерять много баллов.\n\n"
            )
        if "грамматика" in wrong_topics:
            why_text += (
                "📍 В блоке «Грамматика и языковые нормы» (задания 7 и 26 в ЕГЭ: образование форм слов, например родительный падеж, "
                "и анализ средств выразительности) также есть пробелы. Критерии проверки очень строгие, поэтому ошибки здесь сильно бьют по результату.\n\n"
            )
            
        # 5. Скорректирована фраза про вуз ("в выбранный вуз")
        if not why_text:
            why_text = (
                "Прекрасное понимание базовой структуры языка! Однако на высоком уровне каждый балл на вес золота. "
                "Любая помарка из-за стресса в пунктуационном анализе (задание 21) или в критериях сложного сочинения (задание 27) "
                "может лишить тебя места в выбранном вузе.\n\n"
            )

        advantages = (
            "Как мы в Step by Step можем помочь тебе в подготовке:\n"
            "→ работаем с проверенными преподавателями\n"
            "→ подготовим с 0 до нужного результата\n"
            "→ проводим регулярные диагностики в формате экзамена за 12, 9, 6, 3, 2, 1 месяц до ЕГЭ\n"
            "→ направляем развернутую обратную связь от учителей каждый месяц, чтобы ты видел свой прогресс\n"
            "→ готовим индивидуальную домашнюю работу для тебя\n\n"
            "Запишись на полную диагностику с преподавателем, чтобы сдать ЕГЭ на 85+. 👇"
        )
        
        if score <= 4:
            result_text = f"📊 Результат: {score} из {total} правильных ответов.\n🚨 Наш прогноз на ЕГЭ: 35–45 баллов.\n\nПочему такой балл? 🤔\n{why_text}⚠️ ВАЖНОЕ ПРИМЕЧАНИЕ:\nУчти: это была лишь легкая экспресс-диагностика. Чтобы узнать свой точный реальный балл прямо сейчас, пройди полную диагностику с нашим преподавателем.\n\n{advantages}"
        elif score <= 8:
            result_text = f"📊 Результат: {score} из {total} правильных ответов.\n🚨 Наш прогноз на ЕГЭ: 45–55 баллов.\n\nПочему такой балл? 🤔\n{why_text}⚠️ ВАЖНОЕ ПРИМЕЧАНИЕ:\nУчти: это была лишь легкая экспресс-диагностика. Чтобы узнать свой точный реальный балл прямо сейчас, пройди полную диагностику с нашим преподавателем.\n\n{advantages}"
        elif score <= 11:
            result_text = f"📊 Результат: {score} из {total} правильных ответов.\n⚠️ Наш прогноз на ЕГЭ: 60–70 баллов.\n\nПочему такой балл? 🤔\n{why_text}⚠️ ВАЖНОЕ ПРИМЕЧАНИЕ:\nУчти: это была лишь легкая экспресс-диагностика. Чтобы узнать свой точный реальный балл прямо сейчас, пройди полную диагностику с нашим преподавателем.\n\n{advantages}"
        elif score <= 13:
            result_text = f"📊 Результат: {score} из {total} правильных ответов.\n⚠️ Наш прогноз на ЕГЭ: 70–80 баллов.\n\nПочему такой балл? 🤔\n{why_text}⚠️ ВАЖНОЕ ПРИМЕЧАНИЕ:\nУчти: это была лишь легкая экспресс-диагностика. Чтобы узнать свой точный реальный балл прямо сейчас, пройди полную диагностику с нашим преподавателем.\n\n{advantages}"
        else:
            result_text = f"📊 Результат: {score} из {total} правильных ответов.\n🔥 Наш прогноз на ЕГЭ: 80+ баллов! Отличный уровень.\n\nПочему такой балл? 🤔\n{why_text}⚠️ ВАЖНОЕ ПРИМЕЧАНИЕ:\nУчти: это была лишь легкая экспресс-диагностика. Чтобы узнать свой точный реальный балл прямо сейчас, пройди полную диагностику с нашим преподавателем.\n\n{advantages}"
            
        offer_keyboard = InlineKeyboardBuilder()
        offer_keyboard.button(text="🎯 Записаться на диагностику", url="https://t.me/azaretov")
        
        await callback.message.edit_text(
            text=result_text,
            reply_markup=offer_keyboard.as_markup()
        )
        
    await callback.answer()

import os
from aiohttp import web

async def run_polling():
    # Чистый запуск бота в фоновом режиме
    await dp.start_polling(bot)

async def on_startup(app):
    # Привязываем запуск бота к старту сервера без путаницы в аргументах
    asyncio.create_task(run_polling())

def main():
    app = web.Application()
    # Страница-заглушка для прохождения проверки портов Render
    app.router.add_get("/", lambda r: web.Response(text="Bot is running!"))
    app.on_startup.append(on_startup)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == '__main__':
    main()
