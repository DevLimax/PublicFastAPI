from fastapi import HTTPException, status

def UniqueViolationError(field: str, value):
    raise HTTPException(detail=f"Já existe uma instancia com {field}: {value}, portanto não pode haver valores duplicados para esse campo", status_code=status.HTTP_409_CONFLICT)

def NotNullViolationError(field: str, value):
    raise HTTPException(detail=f"O campo {field} deve ser preenchido", status_code=status.HTTP_400_BAD_REQUEST)

