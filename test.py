from src.modules.user.services.hasher_service import Hasher

h = Hasher()
print(h.verify_psw("stringst", "$2b$12$weal45lOmL2gWlau.yB6kuRkBStoMt/R8azjeDqF.T0FeSjTvHXU."))
