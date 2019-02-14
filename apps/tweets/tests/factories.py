import factory
from django.utils import timezone


class TweetsFactory(factory.django.DjangoModelFactory):
    name = 'シナノゴールド'
    tweet_id = factory.Sequence(lambda n: n)
    tweet = '[リンゴ]今日は `シナノゴールド` を食べた。おいしかった。'
    tweeted_at = timezone.now()

    class Meta:
        model = 'tweets.Tweets'


class LastSearchFactory(factory.django.DjangoModelFactory):
    prev_since_id = factory.Sequence(lambda n: n)

    class Meta:
        model = 'tweets.LastSearch'
