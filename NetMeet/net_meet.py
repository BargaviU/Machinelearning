from typing import Tuple
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from chains.custom_chains import (
    get_summary_chain,
    get_interests_chain,
    get_net_meet_chain,
)
from third_parties.linkedin import scrape_linkedin_profile

from third_parties.twitter import scrape_user_tweets
from output_parsers import (
    summary_parser,
    topics_of_interest_parser,
    net_meet_parser,
    Summary,
    NetMeet,
    TopicOfInterest,
)


def net_meet_with(name: str) -> Tuple[Summary, NetMeet, TopicOfInterest, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username)

    summary_chain = get_summary_chain()
    summary_and_facts = summary_chain.run(
        information=linkedin_data, twitter_posts=tweets
    )
    summary_and_facts = summary_parser.parse(summary_and_facts)

    interests_chain = get_interests_chain()
    interests = interests_chain.run(information=linkedin_data, twitter_posts=tweets)
    interests = topics_of_interest_parser.parse(interests)

    net_meet_chain = get_net_meet_chain()
    net_meets = net_meet_chain.run(
        information=linkedin_data, twitter_posts=tweets
    )
    net_meets = net_meet_parser.parse(net_meets)

    return (
        summary_and_facts,
        interests,
        net_meets,
        linkedin_data.get("profile_pic_url"),
    )


if __name__ == "__main__":
    pass