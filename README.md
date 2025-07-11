<img width="900" alt="Image" src="https://github.com/user-attachments/assets/638c0c54-7cb1-4c3e-a374-26b778802fd1" />


**RecycleMeter: A Custom IoT Device for Real-Time Waste Management and Data Analytics**


**Background:** Cultural events are significant to a community, as they provide an opportunity to promote heritage, and diversity, and strengthen community cohesion. While they offer attendees a memorable experience, they tend to generate serious environmental impacts, such as large amounts of waste, high energy consumption, and transportation-related CO2 emissions. Unlike large-scale festivals, small and midsize non-profit festivals often don't practice sustainability initiatives, due to limited budgets, staff, and awareness. The Japan Festival Boston was also one of them since its start in 2012, where no sustainability efforts such as waste separation have been conducted.

**Objective:** To address one of these challenges, we developed “RecycleMeter,” an innovative IoT device that visualizes visitors’ waste sorting contributions in real time. RecycleMeter promotes recycling through proper waste separation, incentivizes environmentally-conscious disposal behavior, and arms organizers with actionable data to refine waste management strategies. By combining technology with education, the project raises sustainability awareness, reduces landfill waste, and embodies the Japanese cultural philosophy of “mottainai,” emphasizing resource mindfulness.

**Methodology:** To develop this smart waste tracking system, we assembled a load cell kit and added a Python code to allow users to select the waste category and automatically calculate the estimated number of collected chopsticks and the reduction in CO2 emissions equivalent from the weight to an open-source driver on GitHub to read the weight. Festival visitors can instantly view their recycling contributions on the website, fostering a sense of involvement and promoting behavioral change. Additionally, organizers gain actionable waste management data to drive future improvements.

**Conclusion:** During the 2025 Japan Festival Boston, RecycleMeter-enabled waste management yielded remarkable outcomes: 150.01 kg of waste was properly sorted over two days, significantly reducing landfill loads. Notably, 56.44 kg (estimated 19,936 pieces) of disposable chopsticks were collected for upcycling, storing 29.24 kg of CO₂ equivalent. Another 93.57 kg of recyclables were responsibly separated. By showcasing numerical “visibility” of environmental contributions, the project merged technology, sustainability, and the Japanese concept of “mottainai,” turning cultural events into platforms for environmental education, proactive behavior, and actionable insights for organizers. The success of RecycleMeter underscores its transformative potential in fostering sustainability in public festivals.

<img width="400" alt="Image" src="https://github.com/user-attachments/assets/9757ff5c-a935-4fe3-acd6-dc4b8377eaa4" /> <img width="400" alt="Image" src="https://github.com/user-attachments/assets/725309be-ce12-4017-9c9c-1c2f1d34f6a5" />

# Demo

[Demo Video](https://drive.google.com/file/d/1zNdhJk-77N_TcD_6_dc9zJlMYPuRLgQ4/view?pli=1)

**Description of the Demo Video:**

First, we placed a garbage bag on the scale and assumed the category is disposable chopsticks. We ran the program, and once it finishes, the terminal displays the weight, estimated CO₂ emissions, and estimated number of chopsticks.

Next, we placed another item on the scale, this time assuming the category is recyclable waste. We ran the program again, and the terminal showed the weight.

When we open the spreadsheet, we can see that the data from both measurements has been recorded automatically.

Next, we checked the website we created. The data for both weighed chopsticks and recyclables is shown there. Each time a new measurement is carried out, the total values are automatically updated.

And we did the same thing at the actual event.
