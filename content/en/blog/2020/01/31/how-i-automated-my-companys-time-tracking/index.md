---
title: How I automated my company's time tracking
summary: In this post I explain the project I developed to automate my company's time tracking
date: 2020-01-31
lastmod: 2025-12-17
tags:
  - timehammer
  - chatbot
  - telegram
  - java
  - kubernetes
  - quarkus
---

## Context

In 2019 there was a change in the law that requires all companies in Spain to provide information about their employees’ working hours, what we commonly know as _time tracking_.

My company adapted to this legislative change by adding a new section to the intranet so that each employee can record their working hours. The approach followed by my company is "real-time" time tracking, meaning that the moment when actions are registered is considered the moment when they are actually performed. This forces employees to clock in at the exact moment they start working, when they start lunch, when they finish lunch, etc. There is no possibility for employees to correct entries themselves; if they forget to register an action, they must send an email to their manager to report it.

This "real-time" approach is not the only possible one. I have seen other companies that also provide a section in their intranet but allow time tracking to be done "after the fact".

Separate questions would be whether these implementations comply with the law, what responsibilities the employee has, or what would happen in the event of an inspection if the employee’s time records are incorrect.

## Problem

The solution adopted by my company is not designed to be comfortable or user-friendly for employees; quite the opposite:

- The employee has to remember all the actions that must be performed
- For certain actions, the employee not only has to perform the action, but also has to write a valid text for that action
- To perform each action, the employee has to access the intranet and enter their credentials
- Some actions are performed in places where there is no computer, so the intranet must be accessed from a mobile phone, even though the intranet is not adapted for mobile use. The menus are very small and it is difficult to reach the time tracking section

## Objective

I set out to simplify this entire process so that time tracking is done in a simple way and as faithfully as possible to reality. In addition, I wanted to use technologies that would allow me to continue developing professionally as a software engineer.

## Requirements

These are the functional requirements that guided the design and development of the solution:

- Time tracking as faithful to reality as possible
- Manual actions required from the user should be very simple
- Time tracking actions performed directly in the intranet will be taken into account

## Solution

The developed solution is a Telegram chatbot: [TimeHammerBot](https://t.me/TimeHammerBot). The only requirement to use it is having a smartphone and the *Telegram* messaging application installed.

An initial solution specific to my company was developed, but it is designed to be easily extensible to any other company (S**O**LID 😉).

## How it works

The employee registers in the [TimeHammerBot](https://t.me/TimeHammerBot) *Telegram* chatbot. During registration, they must specify the company they work for, the credentials to access the intranet where manual time tracking is performed, and their usual schedules: start and end of the working day and start and end of lunch (for each day of the week). Once registered, they can forget about accessing the intranet to record time. From that moment on, the chatbot will remind them at the configured times to perform the corresponding actions. Along with each reminder, a set of buttons is provided to confirm that the actions have been performed.

For example, if the employee indicates that on Mondays they usually start working at 8:00, at that time they will receive a message on *Telegram* asking whether they have already started working. Below the message, a series of buttons will appear: "Yes", "+5m", "+10m", "+15m", "+20m", "No". By pressing the "Yes" button, the chatbot will register the start of the working day in the intranet. By pressing the "+Xm" buttons, the chatbot is instructed to wait X minutes before asking again. By pressing the "No" button, the chatbot is informed that the employee is not working that day and will not ask anything again until the next day.

The chatbot retrieves the employee’s vacation periods from the intranet in order not to disturb them during that time. It also takes into account public holidays in the employee’s work city (which is why the work city must be specified during registration).

The chatbot is merely an intermediary; it never stores the employee’s time tracking data. To determine the employee’s current state, it always retrieves the information from the company’s intranet. This allows the chatbot to be used in combination with manual actions. For example, if an employee has indicated that on Fridays they usually start working at 8:00, but exceptionally starts at 7:30 on a given Friday, they can access the intranet and record their time at 7:30. When 8:00 arrives, the chatbot will take into account any actions performed manually in the intranet before asking anything. In this case, at 8:00 the chatbot will not ask the employee anything.

With this operating model, the three project requirements are fulfilled:

- All time tracking actions require explicit user confirmation and are faithful to reality.
- The user no longer needs to connect to an intranet and manually register actions; instead, they simply press a button when a *Telegram* message arrives.
- By not storing employee state and always retrieving it from the intranet, the system allows both approaches to be combined.

## Architecture

Below are a couple of diagrams showing the existing modules and how they interact with each other:

![Architecture I](./resources/architecture-i.png)

![Architecture II](./resources/architecture-ii.png)

The following table shows the purpose of each module:

| Module                  | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| reverse proxy           | Reverse proxy to manage SSL certificates via Let's Encrypt                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| web                     | Web application for: <ul><li>User registration (company, workplace, usual working and lunch schedules)</li><li>Credential refresh and request</li><ul><li>{{< icon name="hero/information-circle" >}} The main user interaction is through the Telegram application, however, credentials are not requested through that channel. The web application is used instead (with encrypted communication).</li></ul><li>Demos</li></ul>                                                                             |
| scheduler               | Periodically triggers actions, mainly: <ul><li>Updating employee status</li><ul><li>{{< icon name="hero/information-circle" >}} To make the system compatible with exceptional use of the company’s time tracking application</li></ul><li>Updating employee vacations</li><ul><li>{{< icon name="hero/information-circle" >}} To avoid disturbing employees during their vacation periods</li></ul><li>Cleaning up past vacations</li></ul>                                                                   |
| core                    | Connected to the database and responsible for all persistence tasks: <ul><li>Employee registration</li><li>Updating employee preferences</li><li>Retrieving the list of employees working at a given moment</li><li>etc.</li></ul>                                                                                                                                                                                                                                                                             |
| integration             | Routes messages to the specific module for the employee’s company </br></br> {{< icon name="hero/exclamation-circle" >}} When I developed this solution I had no prior experience with EDA architectures. Now I know that this module makes no sense, since messaging brokers are capable of routing messages based on message content                                                                                                                                                                         |
| communytek              | Communication interface with the Comunytek company to register employee actions (start of workday, start of lunch, end of lunch, end of workday, vacation retrieval, etc.) </br></br> {{< icon name="hero/information-circle" >}} Each supported company would have its own module                                                                                                                                                                                                                             |
| statemachine            | Its main responsibilities are: <ul><li>Determining the employee’s state based on a state diagram</li><li>Keeping track of employee waiting periods</li><li>Deciding the next action based on the employee’s state and waiting periods</li></ul>                                                                                                                                                                                                                                                                |
| telegramchatbotnotifier | Sends messages to employees via Telegram                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| telegramchatbot         | Receives messages (both proactive messages and responses) sent by employees via Telegram and injects them into the system                                                                                                                                                                                                                                                                                                                                                                                      |
| commandprocessor        | Processes Telegram commands from employees </br></br> {{< icon name="hero/information-circle" >}} Telegram allows working with a set of commands that avoids having to process free-text messages. This simplifies communication, since free-text messages could be incomplete and require multiple back-and-forth interactions with the employee until the required information is obtained. Telegram allows defining a set of commands for a bot and provides special keyboard buttons to access them easily |

Other modules not shown in the diagram:

| Module   | Purpose                                                                                            |
|----------|----------------------------------------------------------------------------------------------------|
| common   | Shared utilities, converters, serializers, DTOs between different modules, etc.                    |
| catalog  | Manages catalogs: `cities` and `companies`                                                         |
| monolith | Initially the system was developed as a monolith, later it was refactored into an EDA architecture |

For more details about the project, you can visit [here]({{< ref "projects/timehammer" >}})

## Conclusion

This project has been a very interesting challenge for several reasons:

**- Carrying a project through from start to finish**

> The path from having an idea to turning it into reality is always difficult. Along the way there are many moments where the easiest option is not to complicate things and give up. Reaching the point of deploying a first stable and functional version to production is reason enough to feel proud.

**- Facing a new programming paradigm**

> Changing the way you think is not trivial. Tasks you once considered simple suddenly become complex puzzles. At the slightest complication, it is tempting to return to *old habits* just to keep moving forward. Staying *faithful* to reactive programming has been exhausting.

**- New technologies**

> In this project I used many technologies that were new to me: Quarkus, Kafka, EDA, native Java compilation, distroless images. For me, facing a new framework, language, or tool is always motivating—it reminds me of being a child receiving a new toy. The real challenge is building a project where most technologies are unknown and you spend more time reading documentation than writing code.

**- Setting a goal and sticking to it**

> When you don’t have a manager guiding you toward a goal, it’s hard not to stray off course, and it’s very easy to go off on tangents—especially when you have lots of new *"toys"* to try out. This project was no exception; in fact, the final solution is the third one developed from scratch. The project started as serverless, based on Firebase. Then the serverless idea was discarded and it became a monolith developed in Quarkus. Finally, Quarkus was kept, but the system was modularized into an event-driven architecture.

This is a first functional version with plenty of room for improvement. I incorporated a large number of technological novelties, and given my level of experience, I have not yet been able to dive deeply into them in order to deliver this first functional version as quickly as possible.
