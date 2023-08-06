# Author: Shahriar Golchin
# Project: Data Collator for Keyword/Compact Pretraining
# Release Date: 8/28/2022


from transformers import DataCollatorForWholeWordMask

class DataCollatorForKeywordMasking(DataCollatorForWholeWordMask):

  def __init__(self, tokenizer = None, mlm: bool = True, 
               mlm_probability: float = 0.75, pad_to_multiple_of = None, 
               tf_experimental_compile = False, return_tensors = 'pt', list_of_keywords: list = None):
    super().__init__(tokenizer, mlm, mlm_probability, pad_to_multiple_of, tf_experimental_compile, return_tensors)
    
    if list_of_keywords is None:
      self.list_of_keywords = []
    else:
      self.list_of_keywords = list_of_keywords
    
    self.tokenizer = tokenizer
    self.mlm_probability = mlm_probability

  def _whole_word_mask(self, input_tokens, max_predictions=512):
      """
      Get 0/1 labels for masked tokens with whole word mask proxy
      """
      
      list_of_tokens = input_tokens
      list_of_words = self.tokenizer.convert_tokens_to_string(list_of_tokens).split()
      input_tokens_with_kywd_sign = list_of_tokens.copy()


      for word in list_of_words:
        if word in self.list_of_keywords:

          tokenized_keyword = self.tokenizer(word).tokens()
          tokenized_keyword = tokenized_keyword[1:-1] # excluding [CLS] and [SEP]

          for i, token in enumerate(input_tokens_with_kywd_sign):
            if token in tokenized_keyword:
              input_tokens_with_kywd_sign[i] = 'keyword_detected'
      

      # in this section, we get a list of inputs which tokens that create a single word create a single list
      cand_indexes = []
      for (i, token) in enumerate(list_of_tokens):
          if token == "[CLS]" or token == "[SEP]":
              continue
          
          if len(cand_indexes) >= 1 and token.startswith("##"):
              # it creates a list of all the tokens that belong to a single word
              cand_indexes[-1].append(i)
          else:
              # it normally creates a list of all other inputs which each are separate tokens
              cand_indexes.append([i])

      # we don't want to exceed the max number of predictions. maximum of prdictions would be all our input. so, we pick the minimum between a 
      # maximum defined number of predictions and the total input length.
      num_to_predict = min(max_predictions, max(1, int(round(sum(x == "keyword_detected" for x in input_tokens_with_kywd_sign) * self.mlm_probability))))

      # in this part, we collect the indexes of all input with the sign of 'keyword_detected'
      list_of_indexes_to_mask = []
      for i, token in enumerate(input_tokens_with_kywd_sign):
        if token == 'keyword_detected':
          for j, list_of_indexes in enumerate(cand_indexes):
            # check if by adding the list of indexes we won't exceed the maximum prediction length
            #if (len(list_of_indexes) + len(list_of_indexes_to_mask)) > num_to_predict:
              #continue
            for k, index in enumerate(list_of_indexes):
              if cand_indexes[j][k] == i:
                list_of_indexes_to_mask.append(i)

      mask_labels = [1 if i in list_of_indexes_to_mask else 0 for i in range(len(input_tokens))]
      
      return mask_labels