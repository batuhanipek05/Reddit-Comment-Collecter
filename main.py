import praw
from psaw import PushshiftAPI
import datetime as dt
from praw.models import MoreComments


username = "xxxx"  # username for first account
password = "xxxx" # password for first account
client_id = "xxxx" # client id for first account
client_secret = "xxxx" # client secret first account

username2 = "xxxx" # username for first account
password2 = "xxxx" # password for first account
client_id2 = "xxxx" # client id for first account
client_secret2 = "xxx-xxx" # client secret first account




reddit_bot = praw.Reddit(username=username,
                password=password,
                client_id=client_id,
                client_secret=client_secret,
                user_agent="test")

reddidbot2 = praw.Reddit(username=username2,
                            password=password2,
                            client_id=client_id2,
                            client_secret=client_secret2,
                            user_agent="wiki")



# use two diffrent bots to double the speed


def serach_replies(parents, comment):
    rr = []
    if len(comment.replies) > 1 and not isinstance(comment, MoreComments):
        if comment.replies[0].body == "[deleted]" or comment.replies[0].body == "[silinmiş]" \
                or comment.replies[0].body == "[removed]" or comment.replies[0].body == "[silindi]" \
                or "I am a bot and this action" in comment.replies[0].body \
                or "https://" in comment.replies[0].body:
            return rr
        appender = parents + '<end_of_input>' + comment.replies[0].body
        rr.append(appender.replace('\n', " <end_of_line> ").replace('\r', " <end_of_line> "))

        for i in comment.replies:
            if not isinstance(i, MoreComments):
                aaa = serach_replies(parents + ' <end_of_entry> ' + i.body, i)
            else:
                continue
            for i in aaa:
                rr.append(i)
    return rr


def temporarary(id_list, time):
    times = 0
    thins_to_return = []
    for just_a_var in id_list:
        print(times,":::before:::", time)
        if times % 2 == 0:
            submission = reddit_bot.submission(id=just_a_var)
        else:
            submission = reddidbot2.submission(id=just_a_var)
        times += 1
        submission.comments_sort = "top"
        turn = 0
        for i in submission.comments:
            if not isinstance(i, MoreComments):
                if not i.body == "[deleted]" and not i.body == "[silinmiş]" and not i.body == "[removed]" \
                        and not i.body == "[silindi]" and "I am a bot and this action" not in i.body \
                        and "https://" not in i.body:
                    input_texts.append(i.body)
                    if turn == 0:
                        thins_to_return.append(submission.title + '<end_of_input>' + i.body)
                    aa = serach_replies(submission.title + ' <end_of_entry> ' + i.body, i)
                    for j in aa:
                        thins_to_return.append(j.replace('\n', " <end_of_line> ").replace('\r', " <end_of_line> "))
    return thins_to_return







titles = []

input_texts = []
target_texts = []

notepad = open("data.txt", "a")

api = PushshiftAPI()

questions = []


start_epoch = int(dt.datetime(2021, 3, 20).timestamp())

def prepare(start_time=0, limit=0, subreddit="test", count = 500):
    start_epoche = int(dt.datetime(2021, 4, 20).timestamp())
    before = int(dt.datetime(2021, 3, 20).timestamp())
    diff = start_epoche - before
    temp = limit // count
    for i in range(temp):
        a = list(api.search_submissions(sort='desc', sort_type='score', after=start_epoche - diff, before=start_epoche, subreddit=subreddit, limit=limit,
                                        filter=['title', 'selftext']))
        start_epoche = start_epoche - diff - 5
        for i in a:
            title = i.title
            if ("’" in title):
                title = title.replace("’", "\'")
            title = title.replace(" ", "_")
            title = title.replace("\n", "_")
            questions.append(title + "Ğ" + '\n')


def prepareTitleComment(start_time=0, limit=0, subreddit="test", count = 500):
    returned = []
    start_epoche = int(dt.datetime(2021, 4, 1).timestamp())
    before = int(dt.datetime(2021, 3, 1).timestamp())
    diff = start_epoche - before
    #start_epoche = 1566334705
    temp = limit // count
    print(temp)
    for i in range(temp):
        print("STAGE", i)
        a = list(api.search_submissions(sort='desc', sort_type='score', after=start_epoche - diff, before=start_epoche, subreddit=subreddit, limit=count,
                                        filter=['id']))
        print(len(a))
        ids = []
        for j in a:
            if not j.id in ids:
                ids.append(j.id)
        print(ids)
        returned = temporarary(ids, start_epoche)
        with open("data.txt", "a", encoding="utf-8") as g:
            for c5 in returned:
                g.write(c5.replace('\n', " <end_of_line> ").replace('\r', " <end_of_line> ") + "<end_of_data>\n")
        g.close()
        start_epoche = start_epoche - diff - 5
        print("STAGE " + str(i) + "DONE")
    return returned


testReturn = prepareTitleComment(start_time=int(dt.datetime(2021, 4, 20).timestamp()), limit=50000, count=1000, subreddit='AskReddit')





