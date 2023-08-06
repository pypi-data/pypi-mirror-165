import logging
from time import time

from seetm.core.token_mapper import TokenMapper
from seetm.shared.constants import MappingMethod

logger = logging.getLogger(__name__)
tm = TokenMapper(method=MappingMethod.RULE_BASED)


if __name__ == "__main__":
    logger.debug("Started testing the mapper core...")

    text = "castle attitude construct component ConStiTute We are a leading non-state degree awarding " \
           "institute approved by the obesity University Grants Commission (UGC) under the Universities " \
           "Act. We are also members of the A an aviation Association of Commonwealth Universities " \
           "(ACU), as well as the International Association of \"Intel internet calm intercom and the " \
           "first Sri Lankan institute to be accredited by the Institution of Engineering & Technology, UK.\"" \
           "cow love hawk rule bull cool bloom page apple ant degree banana cry requirements dean list " \
           "viva easter barrier Career – In your professional or personal life, you will always be " \
           "asked about your qualifications. If you want to get a good job, then you are supposed " \
           "to have great knowledge in that particular domain, and that is only possible if you have " \
           "acquired a vast amount of knowledge"

    text2 = "SLIIT එකේ තියෙන degrees මොනවද?"

    for t in [text, text2]:
        st = time()
        tm.map(
            data_instance=t,
        )
        et = time()
    print(f"Duration: {et - st}")
