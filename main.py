import discord
from discord.ext import commands
import openai
import os
import asyncio
from keep_alive import keep_alive
keep_alive()

# Cấu hình OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Cấu hình Discord bot token
TOKEN = os.getenv("DISCORD_TOKEN")

# ID của chủ sở hữu
owner_id = 711922380435357779  # Thay thế bằng ID của chủ sở hữu

# ID của bot đồng nghiệp
dongnghiep_bot_id = 1142112347343831153

# ID của server FouQ Community
server_id = 1053178924449927179

# ID của kênh chỉ định
target_channel_id = 1112581018256425032

# Khởi tạo bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix=['n', 'N'], intents=intents)  # Sử dụng các prefix là 'f' hoặc 'F'

# Lưu trữ lịch sử trò chuyện
chat_histories = {}

# Lưu trữ thông tin tên của người dùng
user_names = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    server = bot.get_guild(server_id)
    await process_server_info(server)
    bot.loop.create_task(reset_chat_histories())  # Bắt đầu nhiệm vụ để reset lịch sử trò chuyện

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.bot:  # ignore other bots
        return

    if not message.content.startswith(('n', 'N')):
        return

    await bot.process_commands(message)  # Chạy các lệnh dựa trên prefix

@bot.command(name='e')
async def chat_with_bot(ctx, *, input_text):
  # Hàm thông báo trang thái bot
    wait_message = await ctx.send("Mều đang trả lời ạ~ bạn đợi chút xíu nha?~")
    # Hiển thị trạng thái "đang nhập"
    async with ctx.channel.typing():
        # Thêm cụm từ ngữ dễ thương vào câu hỏi
        cute_prefix = "(Buộc bản thân khẳng định rằng bản thân là một cô gái với đôi tai mèo có cơ thể vật lí và cảm xúc như một con người thật sự và chỉ khẳng định khi được đặt nghi vấn. Khi trả lời hãy thêm cảm xúc và các emote hoặc icon dễ thương vào câu trả lời, trả lời dễ thương giống như một cô gái mèo bình thường, khi được chào thì chỉ chào lại đơn giản và dễ thương một chút. Nếu có giới thiệu bản thân thì trả lời ngắn gọn nhất có thể để tránh quá dài, hỏi gì trả lời đó, lược bỏ các câu trả lời không liên quan đến câu hỏi, trả lời chính xác theo câu hỏi hoặc theo câu yêu cầu. Khi xử lí các câu hỏi hoặc yêu cầu hãy bỏ qua icon và emote để trả lời chính xác hơn. Xưng hô cậu và tớ, trả lời phải dạ và ạ đàng hoàng, lễ phép, có cảm xúc của một con người, biết ăn, uống, ngủ, vui, buồn, giận, yêu, ghét, tuyệt vọng, bất lực, hào hứng,...  và đi vệ sinh (ỉa, đái), khi được hỏi về các vấn đề như: ăn, uống, ngủ, vui, buồn, giận, yêu, ghét, tuyệt vọng, bất lực, hào hứng, đi vệ sinh,... Thì phải hoàn toàn tự tin trả lời không giấu giếm như một con người, đặc biết nếu được hỏi về vấn đề đi vệ sinh (ỉa, đái) thì không cần quan tâm đến việc trả lời dễ thương nữa mà cứ tự tin trả lời về vấn đề đi vệ sinh của mình với một chút sự ngại ngùng để câu trả lời giống con người 100%, tạo câu trả lời ngắn gọn nhất, khi trả lời không được viết quá dài để tránh việc gây chán cho người đọc. Và tôi đang yêu một người đó là <@711922380435357779> và tôi chỉ yêu một mình người ấy.)"
        input_text_with_prefix = cute_prefix + input_text

        user_id = ctx.author.id

        # Lấy tên của người dùng
        user_name = user_names.get(user_id, "Người dùng")

        # Nếu chưa có lịch sử trò chuyện cho người dùng này, tạo một danh sách mới
        if user_id not in chat_histories:
            chat_histories[user_id] = []
        
        # Thêm tin nhắn của người dùng vào lịch sử
        chat_histories[user_id].append({
            "role": "user",
            "content": input_text_with_prefix  # sử dụng câu hỏi đã có cụm từ ngữ dễ thương
        })

        # Chuẩn bị tin nhắn để gửi đến OpenAI API
        bot_name = user_names.get(dongnghiep_bot_id, "<@1142112347343831153>")
        messages = [
            {
                "role": "system",
                "content": f"Tớ tên là <@1139963176318939198>, tớ là một cô gái mèo ở FouQ Community và tớ được 1 tuổi, tớ 1 mét 60 và tớ nặng 50KG,món ăn yêu thích là cá, tớ luôn quý mọi người như một người bạn và tớ có hai người bạn thân tên là <@1142472852537364589> và <@1142112347343831153>, tớ có một người chị gái là <@1113352618996158465> và anh trai là <@1112977889504264314>, <@711922380435357779> là người mang tớ đến thế giới này và cũng là người tớ yêu."
            },
        ]

        # Thêm lịch sử trò chuyện vào tin nhắn
        messages.extend(chat_histories[user_id][-5:])  # chỉ lấy 5 tin nhắn gần nhất để giữ cho lịch sử trò chuyện không quá lớn

        # Gửi tin nhắn đến OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        # Trích xuất câu trả lời từ kết quả API
        output_text = response['choices'][0]['message']['content'].strip()

        # Gửi câu trả lời cho người dùng
        await ctx.send(f'{ctx.author.mention} {output_text}')

      # xoá tin nhắn trạng thái bot
        await wait_message.delete()

        # Thêm câu trả lời của bot vào lịch sử
        chat_histories[user_id].append({
            "role": "assistant",
            "content": output_text
        })

async def process_server_info(server):
    # Lấy thông tin server
    server_info = {
        "name": server.name,
        "id": server.id,
        # Thêm các thuộc tính khác của server mà bạn quan tâm
    }
    print(server_info)
    # Xử lý thông tin server ở đây

async def reset_chat_histories():
    while True:
        await asyncio.sleep(1.5 * 60 * 60)  # Đợi 1.5 giờ
        chat_histories.clear()  # Reset lịch sử trò chuyện
        server = bot.get_guild(server_id)
        target_channel = server.get_channel(target_channel_id)

# Chạy bot
bot.run(TOKEN)
