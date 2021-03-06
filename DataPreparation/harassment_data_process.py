"""
This script pre-processes Harassment dataset by Golbeck et al.
"""
import pandas as pd
import re
import time
from sklearn.utils import resample
from utils import helper_functions as hf


if __name__ == '__main__':

    start = time.time()
    pd.set_option('max_colwidth', 600)
    pd.options.display.max_columns = 10

    data_path = '/Users/soumya/Documents/Mannheim-Data-Science/Sem_4/MasterThesis/Data/'

    harassment_df = pd.read_csv(data_path + 'Online Harassment Dataset/onlineHarassmentDataset_Golbeck.csv', index_col=0, encoding='latin-1')
    # harassment_df = harassment_df.sample(10)

    # harassment_df = harassment_df.dropna(how='all', axis='columns')
    harassment_df = harassment_df.loc[:, ~harassment_df.columns.str.contains('^Unnamed')]

    labels = {'N': 0, 'H': 1}
    harassment_df['code_label'] = harassment_df['Code'].map(labels)
    harassment_df['tweet_processed'] = harassment_df['Tweet'].apply(lambda x: hf.process_tweet(x))

    print(harassment_df.head(10))

    print(pd.Series(harassment_df['tweet_processed']).str.split(' ').str.len().describe())

    raw_tweets = harassment_df.Tweet.values
    processed_tweets = harassment_df.tweet_processed.values

    raw_tweet_2 = []
    for sen in raw_tweets:
        if len(sen.split()) < 120:
            raw_tweet_2.append(sen)

    proc_tweet_2 = []
    for sen in processed_tweets:
        if len(sen.split()) < 120:
            proc_tweet_2.append(len(sen.split()))

    print('Max raw: {}'.format(len(raw_tweet_2)))
    print('Max processed: {}'.format(max(proc_tweet_2)))
    print(proc_tweet_2[:20])

    '''

    df_majority = harassment_df[harassment_df.code_label == 0]
    df_minority = harassment_df[harassment_df.code_label == 1]

    print(df_minority.shape[0])
    # Downsample majority class
    df_majority_downsampled = resample(df_majority,
                                       replace=False,  # sample without replacement
                                       n_samples=df_minority.shape[0],  # to match minority class
                                       random_state=123)  # reproducible results

    # Combine minority class with downsampled majority class
    df_downsampled = pd.concat([df_majority_downsampled, df_minority])

    # Display new class counts
    print(df_downsampled.code_label.value_counts())
    print(df_downsampled.head())

    # print('Max raw: {}'.format(len([sen for sen in raw_tweets if len(sen.split()) < 120])))
    # print('Max processed: {}'.format(len([sen for sen in processed_tweets if len(sen.split()) < 120])))
    '''
    harassment_df.to_csv(data_path + 'Online Harassment Dataset/HarassmentDatasetFull_Golbeck_processed.csv')

    print('Time taken for code execution: {}'.format((time.time() - start)/60))