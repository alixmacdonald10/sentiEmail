import main


if __name__ == "__main__":
    email = "Hi, I placed an order on the 28th June under order no 1000396370. I haven't heard anything since and would appreciate an update or an estimated delivery date. Thanks, Alix"
    scores = main.run(email)
    main.plot_scores(scores)
    sentiment = main.sentiment_func(scores)
    print(f'Sentiment is {sentiment}!')
    